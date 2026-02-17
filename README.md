---
title: YouTube Comment Sentiment Analyzer
emoji: 🎬
colorFrom: blue
colorTo: purple
sdk: docker
app_file: Dockerfile
pinned: false
---

# 🎬 YouTube Comment Sentiment Analyzer

<p align="center">
  <img src="extension\analysis.png" alt="Project Logo" width="120" height="120">
</p>

<p align="center">
  <strong>A smart Chrome extension that analyzes the sentiment of YouTube comments using a fine-tuned DistilBERT model.</strong><br>
  <em>Built with 🧠 Deep Learning, ⚡ ONNX Runtime, and 🐍 Flask</em>
</p>

---

## 👨‍💻 About the Author & Project

<p align="left">
  <strong>Faraz Khan</strong><br>
  <em>BS Artificial Intelligence (5th Semester)</em><br>
  University of Engineering and Applied Sciences (UEAS), Swat
</p>

This project was developed as the **semester project** for the course **Artificial Neural Networks & Deep Learning**. It demonstrates the end-to-end process of fine-tuning a transformer model, deploying it with ONNX Runtime, and creating a real-world Chrome extension.

<p align="left">
  <a href="https://github.com/FarazKhanAI">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
  </a>
  <a href="https://www.linkedin.com/in/faraz-khan-fa23bsai20">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
  </a>
  <a href="https://github.com/FarazKhanAI/yt_sentiment_analysis">
    <img src="https://img.shields.io/badge/Repository-📁-blue?style=for-the-badge" alt="Repository">
  </a>
  <a href="https://huggingface.co/spaces/Zoro828/yt-sentiment-analysis">
    <img src="https://img.shields.io/badge/Live%20Demo-🤗-yellow?style=for-the-badge&logo=huggingface&logoColor=black" alt="Hugging Face">
  </a>
</p>

---

## 📋 Table of Contents

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-model-performance">Model Performance</a> •
  <a href="#-project-structure">Structure</a> •
  <a href="#-quick-start-local">Local Setup</a> •
  <a href="#-deploy-on-hugging-face">Hugging Face Deploy</a> •
  <a href="#-extension-usage">Usage</a>
</p>

---

## ✨ Features

- 🧠 **AI-Powered Analysis**: Fine-tuned DistilBERT model (converted to ONNX) classifies comments as **Positive**, **Neutral**, or **Negative**.
- ⚡ **Blazing Fast on CPU**: Optimized with ONNX Runtime and batch processing for quick inference without a GPU.
- 📊 **Real-Time Progress**: The extension popup shows live status – fetching comments, analyzing, and final results.
- 🔗 **Fetches All Comments**: Uses YouTube Data API v3 to retrieve both top-level comments and their replies (up to 500).
- 🌐 **Cloud-Ready**: Comes with a `Dockerfile` for seamless deployment on Hugging Face Spaces or any cloud platform.
- 🎨 **Modern UI**: Clean, gradient-styled popup with clear sentiment counts and a refresh button.

---

## 📈 Model Performance

The core sentiment model was fine-tuned on a large dataset of **~1 million YouTube comments** and evaluated on a held-out test set of ~150,000 comments.

| Metric | Negative | Neutral | Positive | Overall |
|--------|----------|---------|----------|---------|
| **Precision** | 0.76 | 0.71 | 0.80 | **0.76** |
| **Recall**    | 0.79 | 0.70 | 0.79 | **0.76** |
| **F1-Score**  | 0.77 | 0.71 | 0.79 | **0.76** |

- **Overall Accuracy**: **75.8%**
- **Weighted F1-Score**: **0.758**

The model performs best on positive and negative comments, which often contain strong emotional cues. Neutral comments are inherently more challenging but still achieve solid results.

> **Note**: The model is optimized for CPU inference. You can download it from the [project's Google Drive folder](https://drive.google.com/drive/folders/1-iF9RJ8inD_HGmlNKK7BK-yS-Gx8Jz6Z?usp=sharing).

---

## 📁 Project Structure

```
yt_sentiment_analysis/
├── backend/                          # Flask API + ML model
│   ├── app.py                        # Main Flask application with job queue
│   ├── utils.py                       # SentimentAnalyzer class & YouTube API helpers
│   ├── requirements.txt                # Python dependencies
│   ├── __init__.py                     # Makes 'backend' a package
│   └── model/                          # (Not in repo – download separately)
│       ├── model.onnx                  # DistilBERT in ONNX format
│       ├── tokenizer.json, vocab.txt   # Tokenizer files
│       ├── tokenizer_config.json
│       └── label_map.json               # Sentiment label mappings
│
├── extension/                         # Chrome extension source
│   ├── manifest.json                   # Extension config (Manifest V3)
│   ├── background.js                    # Service worker for API calls
│   ├── content.js                       # Extracts video ID from YouTube
│   ├── popup.html                        # Extension popup UI
│   ├── popup.css                         # Popup styling
│   ├── popup.js                          # Popup logic & polling
│   └── icons.png                          # Extension icon
│
├── Dockerfile                           # Production container for Hugging Face
├── .env.example                          # Template for environment variables
├── .gitignore
└── README.md                             # You are here!
```

---

## 🚀 Quick Start (Local Development)

Follow these steps to run the project on your own machine.

### Prerequisites
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (Python 3.11+)
- Google Chrome browser
- A [YouTube Data API v3 key](https://console.cloud.google.com/) (enable the YouTube Data API v3)

### Step 1: Clone the Repository
```bash
git clone https://github.com/FarazKhanAI/yt_sentiment_analysis.git
cd yt_sentiment_analysis
```

### Step 2: Set Up Python Environment
```bash
conda create -n yt_sentiment python=3.11 -y
conda activate yt_sentiment
pip install -r backend/requirements.txt
```

### Step 3: Add Your YouTube API Key
Create a `.env` file in the project root (or set the environment variable directly):
```bash
echo "YOUTUBE_API_KEY=YOUR_API_KEY_HERE" > .env
```

### Step 4: Download the Model Files
The model files are **too large for GitHub**. Download them from the [Google Drive folder](https://drive.google.com/drive/folders/1-iF9RJ8inD_HGmlNKK7BK-yS-Gx8Jz6Z?usp=sharing) and place them inside `backend/model/`.  
Ensure the folder contains:
- `model.onnx` (the quantized model is also fine)
- `tokenizer.json`, `tokenizer_config.json`, `vocab.txt`
- `label_map.json`

### Step 5: Run the Flask Backend
```bash
cd backend
python app.py
```
You should see: `* Running on http://127.0.0.1:5000`

### Step 6: Load the Extension in Chrome
1. Open Chrome and go to `chrome://extensions/`.
2. Enable **Developer mode** (toggle in top-right).
3. Click **Load unpacked** and select the `extension/` folder.
4. The extension icon will appear in your toolbar.

### Step 7: Test It!
- Visit any YouTube video (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`).
- Click the extension icon. You'll see live progress, and after a few seconds, the sentiment counts will appear.

---

## ☁️ Deploy on Hugging Face Spaces

Your project is already live at [https://huggingface.co/spaces/Zoro828/yt-sentiment-analysis](https://huggingface.co/spaces/Zoro828/yt-sentiment-analysis). Here's how you can replicate it or deploy your own version.

### 1. Create a New Space
- Go to [huggingface.co/spaces](https://huggingface.co/spaces)
- Click **Create new Space**
- Choose **Docker** as the Space SDK
- Name it (e.g., `yt-sentiment-analysis`)
- Set visibility (public or private)

### 2. Upload Project Files
Via the Hugging Face web interface:
- Upload all files from your local project **except** `.git` and `.env`.
- **Crucially**, upload the `backend/model/` folder with all model files. This is the only large folder.

### 3. Set Environment Secrets (Not Files!)
- Go to the **Settings** tab of your Space.
- Under **Repository secrets**, add:
  - **Name**: `YOUTUBE_API_KEY`
  - **Value**: Your actual YouTube API key
- **Do not** upload a `.env` file – secrets are more secure.

### 4. Build & Run
The Space will automatically build using the `Dockerfile`. After a few minutes, your app will be live at:  
`https://<your-username>-<space-name>.hf.space`  
(For example, `https://zoro828-yt-sentiment-analysis.hf.space`)

### 5. Update the Extension for Cloud Use
In your local `extension/` folder, edit these files to point to your live Space:
- `background.js`: Change `API_BASE` to your Space URL.
- `popup.js`: Change the `API_BASE` in the polling function.

Then reload the extension in Chrome.

---

## 🧩 How to Use the Extension

1. **Navigate** to any YouTube video with comments enabled.
2. **Click** the extension icon in your Chrome toolbar.
3. **Watch** the progress:
   - "Fetching comments..." (count updates as comments load)
   - "Analyzing comments..." (shows progress like 150/300)
4. **View results**:
   - The popup displays counts for Positive, Neutral, and Negative comments.
   - A warning may appear if the API quota is exceeded or comments are disabled.
5. **Refresh** by clicking the button to re-analyze (e.g., after scrolling to load more comments).

---

## 🔧 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `YOUTUBE_API_KEY` | Your YouTube Data API v3 key | **Yes** |
| `PORT` | Port for Flask (default: 5000) | No |

- For **local development**, use a `.env` file in the project root.
- For **Hugging Face**, set these as **Secrets** in your Space settings.

---

## 🧪 API Endpoints (For Developers)

The backend exposes two simple REST endpoints:

- **`POST /analyze_video`**  
  Starts analysis. Expects JSON: `{ "video_id": "..." }` or `{ "video_url": "..." }`.  
  Returns: `{ "job_id": "uuid" }`

- **`GET /job/<job_id>`**  
  Polls for job status. Returns progress, and eventually results:
  ```json
  {
    "status": "complete",
    "results": {
      "positive": 42,
      "neutral": 105,
      "negative": 23,
      "total": 170
    },
    "warning": "optional message"
  }
  ```

---

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details (if included).

---

## 🙏 Acknowledgements

- [Hugging Face Transformers](https://huggingface.co/transformers/) for the amazing library and model hub.
- [ONNX Runtime](https://onnxruntime.ai/) for cross-platform, high-performance inference.
- [Google YouTube Data API](https://developers.google.com/youtube/v3) for providing access to comments.
- Kaggle for the GPU time to train the model.

---

<p align="center">Made with ❤️ and a lot of ☕ by Faraz Khan</p>
