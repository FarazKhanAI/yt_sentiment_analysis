import os
import json
import re
import numpy as np
import onnxruntime as ort
from transformers import DistilBertTokenizer
from googleapiclient.discovery import build

class SentimentAnalyzer:
    def __init__(self, model_folder='model', onnx_filename='model.onnx'):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(base_dir, model_folder)
        self.onnx_path = os.path.join(self.model_path, onnx_filename)

        self.tokenizer = DistilBertTokenizer.from_pretrained(self.model_path)
        self.session = ort.InferenceSession(self.onnx_path)
        with open(os.path.join(self.model_path, 'label_map.json'), 'r') as f:
            self.label_map = json.load(f)
        self.id_to_sentiment = {v: k for k, v in self.label_map.items()}

    def predict_batch(self, texts, batch_size=32):
        sentiments = []
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            inputs = self.tokenizer(
                batch_texts,
                truncation=True,
                padding='max_length',
                max_length=128,
                return_tensors='np'
            )
            ort_inputs = {
                'input_ids': inputs['input_ids'].astype(np.int64),
                'attention_mask': inputs['attention_mask'].astype(np.int64)
            }
            outputs = self.session.run(None, ort_inputs)
            logits = outputs[0]
            pred_ids = np.argmax(logits, axis=1)
            sentiments.extend([self.id_to_sentiment[pid] for pid in pred_ids])
        return sentiments

def extract_video_id(url):
    patterns = [
        r'(?:youtu\.be\/)([a-zA-Z0-9_-]{11})',
        r'(?:watch\?v=)([a-zA-Z0-9_-]{11})',
        r'(?:embed\/)([a-zA-Z0-9_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def fetch_comments_from_api(video_id, api_key, max_results=500):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []
    next_page_token = None
    total_fetched = 0
    warning = None

    try:
        while total_fetched < max_results:
            request = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                maxResults=min(100, max_results - total_fetched),
                pageToken=next_page_token,
                textFormat='plainText'
            )
            response = request.execute()

            for item in response['items']:
                top_comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(top_comment)
                total_fetched += 1

                if 'replies' in item:
                    for reply_item in item['replies']['comments']:
                        if total_fetched >= max_results:
                            break
                        reply_text = reply_item['snippet']['textDisplay']
                        comments.append(reply_text)
                        total_fetched += 1

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
    except Exception as e:
        error_msg = str(e)
        if 'quotaExceeded' in error_msg:
            warning = "API quota exceeded. Showing partial results."
        elif 'commentsDisabled' in error_msg:
            warning = "Comments are disabled for this video."
        else:
            warning = f"API error: {error_msg}"

    return comments, warning