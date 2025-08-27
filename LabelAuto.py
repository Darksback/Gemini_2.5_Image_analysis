import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image
import google.generativeai as genai
import csv
import os
import threading
import queue
import time
import json

# --- Configuration ---
RPM_LIMIT = 10
NUM_WORKERS = 5
MAX_RETRIES = 2
SECONDS_PER_REQUEST = 60.0 / RPM_LIMIT

# --- Thread-Safe Rate Limiter & Token Dispenser ---
api_rate_limiter = threading.Semaphore(0)
def token_dispenser():
    while True:
        api_rate_limiter.release()
        time.sleep(SECONDS_PER_REQUEST)

# --- Configure API Key and Model ---
try:
    # IMPORTANT: Replace "YOUR_API_KEY" with your actual Gemini API key
    genai.configure(api_key="YOUR_API_KEY")
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    messagebox.showerror("API Configuration Error", f"Fatal API Error: {e}")
    exit()

# --- Analysis Function ---
def analyze_image_with_gemini(image_path, result_queue):
    """
    Asks Gemini for a JSON object containing both tracking and phone numbers.
    """
    filename = os.path.basename(image_path)
    last_error = "Unknown Error"
    for attempt in range(MAX_RETRIES):
        try:
            api_rate_limiter.acquire()
            optimized_img = Image.open(image_path)
            optimized_img.thumbnail((1024, 1024))
            prompt = (
                "Analyze the shipping label image and act as a JSON API. Your task is to extract two specific pieces of information:\n"
                "1. `tracking_number`: Find the tracking number. It should start with 'CON', '1Z', '5904', or 'DOM'.\n"
                "2. `phone_number`: Find the phone number located ONLY in the recipient's address block (the 'TO:' block). Do not use the sender's phone number.\n\n"
                "Return your findings as a single, valid JSON object. If a value is not found, use 'NONE' as the string value for that key. Your entire response should be only the JSON object, with nothing before or after it.\n"
                "Example: {\"tracking_number\": \"CON123456789012345678\", \"phone_number\": \"(555) 123-4567\"}"
            )
            response = model.generate_content([prompt, optimized_img])
            cleaned_text = response.text.strip().replace("```json", "").replace("```", "")
            data = json.loads(cleaned_text)
            tracking = data.get("tracking_number", "NONE").strip()
            phone = data.get("phone_number", "NONE").strip()
            result_queue.put({"filename": filename, "tracking": tracking, "phone": phone, "error": None})
            return
        except Exception as e:
            last_error = f"Error: {str(e)}"
            time.sleep(1 + attempt)
            continue
    result_queue.put({"filename": filename, "tracking": "FAIL", "phone": "FAIL", "error": last_error})

# --- GUI and Worker Management ---
def select_images_and_process():
    file_paths = filedialog.askopenfilenames(
        title="Select Shipping Label Images",
        filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*"))
    )
    if not file_paths: return
    select_button.config(state=tk.DISABLED)
    export_button.config(state=tk.DISABLED)
    results_text.delete(1.0, tk.END)
    root.results_to_export = []
    file_queue = queue.Queue()
    for fp in file_paths: file_queue.put(fp)
    result_queue = queue.Queue()
    threading.Thread(target=process_results_queue, args=(result_queue, len(file_paths)), daemon=True).start()
    for _ in range(NUM_WORKERS):
        threading.Thread(target=worker, args=(file_queue, result_queue), daemon=True).start()

def worker(file_q, result_q):
    while not file_q.empty():
        try:
            file_path = file_q.get_nowait()
            analyze_image_with_gemini(file_path, result_q)
        except queue.Empty:
            break

def process_results_queue(result_q, total_files):
    processed_count = 0
    while processed_count < total_files:
        try:
            result = result_q.get(timeout=1.0)
            results_text.insert(tk.END, f"File: {result['filename']}\n")
            if result['error']:
                 results_text.insert(tk.END, f"  -> ERROR: {result['error']}\n\n")
            else:
                results_text.insert(tk.END, f"  -> Tracking Number: {result['tracking']}\n")
                results_text.insert(tk.END, f"  -> Phone Number: {result['phone']}\n\n")
            root.results_to_export.append(result)
            processed_count += 1
        except queue.Empty:
            continue
    select_button.config(state=tk.NORMAL)
    export_button.config(state=tk.NORMAL)

def export_to_csv():
    """
    Exports to CSV, applying conditional logic and forcing text format for the final value.
    """
    if not hasattr(root, 'results_to_export') or not root.results_to_export:
        messagebox.showwarning("No Data", "There is no data to export.")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save Final Data to CSV")
    if not save_path: return

    final_data_for_csv = []
    sorted_results = sorted(root.results_to_export, key=lambda x: x['filename'])

    for result in sorted_results:
        tracking_num = result.get('tracking', 'NONE')
        if tracking_num in ["FAIL", None]: tracking_num = "NONE"

        phone_num = result.get('phone', 'NONE')
        if phone_num in ["FAIL", None]: phone_num = "NONE"

        is_con_too_short = tracking_num.startswith("CON") and len(tracking_num) < 19
        is_tracking_valid = tracking_num != 'NONE' and not is_con_too_short

        final_value = "NONE"
        if is_tracking_valid:
            final_value = tracking_num
        elif phone_num != 'NONE':
            final_value = phone_num

        # **MODIFICATION HERE: Force text format for CSV**
        # This wraps the value in `="..."` to prevent spreadsheet auto-formatting.
        formatted_value_for_csv = f'="{final_value}"'

        final_data_for_csv.append({"Filename": result['filename'], "Tracking Number": formatted_value_for_csv})

    try:
        with open(save_path, 'w', newline='') as csvfile:
            fieldnames = ["Filename", "Tracking Number"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(final_data_for_csv)
        messagebox.showinfo("Success", f"Final data was successfully exported to:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Export Error", f"An error occurred while exporting:\n{e}")

# --- GUI Setup ---
root = tk.Tk()
root.title("Gemini Data Extractor (10 RPM)")
root.geometry("600x500")

threading.Thread(target=token_dispenser, daemon=True).start()

main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)
control_frame = tk.Frame(main_frame, pady=10)
control_frame.pack(fill=tk.X)
select_button = tk.Button(control_frame, text="Select Images and Analyze", command=select_images_and_process, width=25)
select_button.pack(side=tk.LEFT, padx=(0, 10))
export_button = tk.Button(control_frame, text="Export to CSV", command=export_to_csv, width=15, state=tk.DISABLED)
export_button.pack(side=tk.LEFT)
results_label = tk.Label(main_frame, text="Results:")
results_label.pack(anchor='w')
results_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=15)
results_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

root.mainloop()