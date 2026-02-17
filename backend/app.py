import os
import uuid
from dotenv import load_dotenv
import threading
import time
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from utils import SentimentAnalyzer, fetch_comments_from_api, extract_video_id


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

analyzer = SentimentAnalyzer()


YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')


jobs = {}

def background_worker(job_id, video_id):
    """Run fetch + analysis in background, updating job status."""
    jobs[job_id]['status'] = 'fetching'
    jobs[job_id]['message'] = 'Fetching comments...'
    jobs[job_id]['fetched'] = 0

    # Fetch comments (including replies)
    comments, warning = fetch_comments_from_api(video_id, YOUTUBE_API_KEY, max_results=500)
    jobs[job_id]['fetched'] = len(comments)

    if not comments:
        jobs[job_id]['status'] = 'error'
        jobs[job_id]['message'] = warning or 'No comments found.'
        return

    jobs[job_id]['status'] = 'analyzing'
    jobs[job_id]['message'] = f'Analyzing {len(comments)} comments...'
    jobs[job_id]['total'] = len(comments)
    jobs[job_id]['processed'] = 0

    # Analyze in batches, update progress
    batch_size = 32
    sentiments = []
    for i in range(0, len(comments), batch_size):
        batch = comments[i:i+batch_size]
        batch_sentiments = analyzer.predict_batch(batch)
        sentiments.extend(batch_sentiments)
        jobs[job_id]['processed'] = min(i + batch_size, len(comments))
        # Optionally update counts incrementally, but we'll just show processed count

    # Count sentiments
    results = {'positive': 0, 'neutral': 0, 'negative': 0}
    for s in sentiments:
        results[s.lower()] += 1
    results['total'] = len(comments)

    jobs[job_id]['status'] = 'complete'
    jobs[job_id]['results'] = results
    if warning:
        jobs[job_id]['warning'] = warning

@app.route('/analyze_video', methods=['POST'])
def analyze_video():
    data = request.get_json()
    video_url = data.get('video_url', '')
    video_id = data.get('video_id', '')

    if not video_id and video_url:
        video_id = extract_video_id(video_url)

    if not video_id:
        return jsonify({'error': 'Invalid or missing video ID/URL'}), 400

    # Create a new job
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        'id': job_id,
        'video_id': video_id,
        'status': 'queued',
        'message': 'Queued...',
        'created_at': time.time()
    }

    # Start background thread
    thread = threading.Thread(target=background_worker, args=(job_id, video_id))
    thread.daemon = True
    thread.start()

    return jsonify({'job_id': job_id})

@app.route('/job/<job_id>', methods=['GET'])
def get_job_status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404

    # Return relevant fields based on status
    response = {
        'job_id': job_id,
        'status': job['status'],
        'message': job.get('message', '')
    }
    if job['status'] == 'fetching':
        response['fetched'] = job.get('fetched', 0)
    elif job['status'] == 'analyzing':
        response['processed'] = job.get('processed', 0)
        response['total'] = job.get('total', 0)
    elif job['status'] == 'complete':
        response['results'] = job.get('results')
        if 'warning' in job:
            response['warning'] = job['warning']
    elif job['status'] == 'error':
        response['error'] = job.get('message')

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)