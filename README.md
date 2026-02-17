# YouTube Comment Sentiment Analyzer

A Chrome extension that analyzes the sentiment of YouTube video comments using a fine‑tuned DistilBERT model (exported to ONNX for fast CPU inference). The backend runs a Flask API that loads the model and returns sentiment counts.

## Features
- Extracts video title and comments from the current YouTube page.
- Sends comments to a local Flask API.
- Displays counts of positive, neutral, and negative comments in a clean popup.
- Uses ONNX Runtime for efficient CPU inference.

## Project Structure
```
YT_sentiment_analysis/
├── backend/               # Flask API and model
│   ├── app.py
│   ├── requirements.txt
│   ├── utils.py
│   └── model/             # ONNX model & tokenizer files
├── extension/             # Chrome extension source
│   ├── manifest.json
│   ├── background.js
│   ├── content.js
│   ├── popup.html
│   ├── popup.css
│   ├── popup.js
│   └── icons.png
└── README.md
```

## Prerequisites
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (Python 3.11+)
- Google Chrome browser

## Setup Instructions

### 1. Create and Activate Conda Environment
```bash
cd F:\YT_sentiment_analysis
conda create -n yt_sentiment python=3.11 -y
conda activate yt_sentiment
```

### 2. Install Backend Dependencies
```bash
pip install -r backend/requirements.txt
```

### 3. Place the Model Files
Ensure the `backend/model/` folder contains:
- `model_quantized.onnx` (or `model.onnx`)
- `tokenizer.json`, `tokenizer_config.json`, `vocab.txt`
- `label_map.json`

These files were generated during the Kaggle training and export steps.

### 4. Start the Flask Server
```bash
cd backend
python app.py
```
The API will be available at `http://localhost:5000`.

### 5. Load the Extension in Chrome
1. Open Chrome and go to `chrome://extensions/`
2. Enable **Developer mode** (toggle in top‑right).
3. Click **Load unpacked** and select the `extension` folder.
4. The extension icon should appear in the toolbar.

### 6. Use the Extension
- Navigate to any YouTube video (e.g., `https://www.youtube.com/watch?v=...`).
- Wait for comments to load (scroll down if needed).
- Click the extension icon – a popup will show the sentiment analysis results.
- Click **Refresh Analysis** to re‑analyze (e.g., after loading more comments).

## Notes
- The Flask server must be running locally while using the extension.
- For production deployment, consider hosting the API on a cloud service and update the fetch URL in `background.js`.
- The model is optimized for CPU inference via ONNX Runtime. If you experience slow performance, try using the quantized model (`model_quantized.onnx`).

## Troubleshooting
- **"Cannot communicate with page"**: Refresh the YouTube tab and ensure the content script is injected (check extension permissions).
- **API connection refused**: Make sure Flask is running on port 5000 and no firewall is blocking it.
- **No comments found**: YouTube comments load dynamically; scroll down to load more comments before clicking the extension.

## License
MIT


---

## 5. Final Steps

1. **Run the backend** (in a terminal with the conda environment activated):
   ```bash
   cd backend
   python app.py
   ```
2. **Load the extension** in Chrome as described.
3. **Test** on a YouTube video.
