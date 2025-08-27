# Gemini_2.5_Image_analysis
A python script using the Google Ai Gemini 2.5 Flash for Text and data extraction from images.
Gemini AI Shipping Label Extractor
This is a Python application with a graphical user interface (GUI) designed to automate the extraction of data from images of shipping labels. It leverages the power of Google's Gemini AI to intelligently find tracking numbers and phone numbers, processes images in bulk, and exports the final, clean data to a CSV file.
The application is built to be robust, efficient, and respectful of API limits, making it a powerful tool for logistics, e-commerce, or anyone needing to digitize information from shipping labels.
Features
Bulk Image Processing: Select and process multiple image files (.jpg, .png) at once.
AI-Powered Extraction: Uses the Google Gemini 1.5 Flash model to analyze images and extract data.
Dual Data Extraction: For each label, it intelligently identifies both the tracking number and the recipient's phone number.
Detailed GUI: A user-friendly interface displays the extracted tracking number and phone number for each image in real-time, allowing for immediate review.
Conditional Logic for CSV Export: The final CSV output is clean and follows specific business rules:
The tracking number is the primary data point.
If a valid tracking number isn't found, the recipient's phone number is used as a fallback.
A tracking number starting with "CON" must be at least 19 characters long to be considered valid.
Strict API Rate Limiting: Guarantees that the application never exceeds 10 requests per minute (RPM), preventing API errors and ensuring stable operation.
Correct CSV Formatting: Automatically formats the tracking number column as text in the CSV file to prevent spreadsheet programs (like Excel) from corrupting long numbers with scientific notation.
Efficient & Robust: Utilizes multi-threading for fast processing and includes an automatic retry mechanism to handle temporary network or API errors gracefully.
Prerequisites
Before you can run this application, you will need the following:
Python 3.7+: Make sure Python is installed on your system. You can download it from python.org.
Google Gemini API Key: You need an API key to use the Gemini model. You can get one for free from Google AI Studio.
Required Python Libraries: You will need google-generativeai and Pillow.
Installation
Follow these steps to set up the application on your machine.
Download the Script:
Save the Python code as a file named app.py (or any other .py name) on your computer.
Install Libraries:
Open your terminal or command prompt and run the following command to install the necessary packages:
code
Bash
pip install google-generativeai pillow
Configuration
Before running the script for the first time, you must configure it with your Gemini API key.
Open the Python script (app.py) in a text editor.
Find this line near the top of the file:
code
Python
genai.configure(api_key="YOUR_API_KEY")
Replace "YOUR_API_KEY" with the actual API key you obtained from Google AI Studio.
(Optional) Adjust Settings:
You can also tune the RPM_LIMIT and NUM_WORKERS variables at the top of the script if you have different API limits or want to adjust performance. The default of 10 RPM is safe for the free tier.
How to Use
Run the Application:
Open your terminal or command prompt, navigate to the directory where you saved the script, and run:
code
Bash
python app.py
Select Images:
Click the "Select Images and Analyze" button. A file dialog will open, allowing you to select one or more shipping label images.
Review Results:
The application will begin processing the images. In the main window, you will see the extracted Tracking Number and Phone Number for each file as they are completed.
Export to CSV:
Once all images have been processed, the "Export to CSV" button will become active. Click it.
Save the File:
A dialog will ask you where you want to save the final CSV file. Choose a location and a name. The resulting file will contain two columns: Filename and Tracking Number, with the data populated according to the conditional logic.
