# Gemini AI Shipping Label Extractor

A Python application that automatically extracts tracking numbers and phone numbers from shipping label images using Google's Gemini AI API.

## Features

- **AI-Powered Analysis**: Uses Google Gemini 2.5 Flash model for accurate text extraction, and cost effectivity
- **Batch Processing**: Process multiple images simultaneously with configurable worker threads
- **Rate Limiting**: Built-in API rate limiting (10 RPM) to comply with Gemini API limits
- **Smart Data Extraction**: Automatically identifies tracking numbers and recipient phone numbers
- **Export Functionality**: Export results to CSV format with proper formatting
- **User-Friendly GUI**: Simple Tkinter interface for easy operation
- **Error Handling**: Robust error handling with retry mechanisms

## Requirements

- Python 3.7+
- Google Gemini API key
- Internet connection for API access

## Installation

1. **Clone or download the script**
2. **Install required packages:**
   ```bash
   pip install google-generativeai pillow
   ```

3. **Get a Google Gemini API key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the API key

4. **Configure the API key:**
   - Open `LabelAuto.py`
   - Replace `"YOUR_API_KEY"` on line 30 with your actual API key

## Usage

### Running the Application

```bash
python LabelAuto.py
```

### How to Use

1. **Launch the application** - A GUI window will appear
2. **Click "Select Images and Analyze"** - Choose shipping label images (JPG, PNG)
3. **Wait for processing** - The AI will analyze each image
4. **Review results** - See extracted data in the results window
5. **Export to CSV** - Click "Export to CSV" to save results

### Supported Image Formats

- JPEG (.jpg)
- PNG (.png)
- Other formats (may work but not guaranteed)

## Configuration

### Rate Limiting
- **Default**: 10 requests per minute (RPM)
- **Workers**: 5 concurrent processing threads
- **Retries**: 2 attempts per image on failure

### API Model
- **Model**: Gemini 1.5 Flash
- **Image Processing**: Automatically resized to 1024x1024 for optimal performance

## Output Format

The application extracts two main data points:

1. **Tracking Number**: 
   - Looks for numbers starting with 'CON', '1Z', '5904', or 'DOM'
   - Validates CON numbers are at least 19 characters

2. **Phone Number**: 
   - Extracts from recipient address block only
   - Excludes sender phone numbers

### CSV Export Format
- **Filename**: Original image filename
- **Tracking Number**: Extracted tracking number or phone number (if tracking unavailable)
- **Format**: Values are wrapped in `="..."` to prevent spreadsheet auto-formatting

## Error Handling

- **API Failures**: Automatic retry with exponential backoff
- **Image Processing**: Graceful handling of corrupted or unsupported images
- **Network Issues**: Timeout handling and connection error recovery

## Performance

- **Processing Speed**: ~6 seconds per image (with rate limiting)
- **Batch Size**: Recommended 50-100 images per session
- **Memory Usage**: Efficient image processing with automatic resizing

## Troubleshooting

### Common Issues

1. **"API Configuration Error"**
   - Check your API key is correctly set
   - Verify internet connection

2. **"Import google.generativeai could not be resolved"**
   - Run: `pip install google-generativeai`

3. **Slow Processing**
   - Reduce number of workers (modify `NUM_WORKERS` variable)
   - Check API rate limits

4. **Export Failures**
   - Ensure you have write permissions in the target directory
   - Check if the file is open in another application

## Limitations

- Requires active internet connection
- Subject to Google Gemini API rate limits
- Image quality affects extraction accuracy
- Best results with clear, high-resolution shipping labels

## License

This project is open source. Feel free to modify and distribute.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your API key and internet connection
3. Ensure all dependencies are properly installed

## Version

Current version: 1.0
Last updated: 2025

