import csv
from collections import defaultdict
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from URL_Detection import url_detection
from Review_Analysis import classify_review
import os
from threading import Lock

app = Flask(__name__)
CORS(app)

FAKE_REVIEW_LOG = 'E-Commerce API/fake_reviews_log.csv'
log_lock = Lock()

def get_daily_fake_review_counts():
    daily_counts = defaultdict(int)
    if not os.path.exists(FAKE_REVIEW_LOG):
        return daily_counts  # Return empty if file doesn't exist

    with open(FAKE_REVIEW_LOG, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            review_text, timestamp = row
            date_str = timestamp.split()[0]  # Extract date from timestamp
            daily_counts[date_str] += 1
    return daily_counts

def log_fake_review(review_text):
    with log_lock:
        with open(FAKE_REVIEW_LOG, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([review_text, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

# API route to handle combined review and URL analysis
@app.route('/api/combined_review_analysis', methods=['POST'])
def combined_review_analysis():
    try:
        data = request.json
        review_text = data.get('review_text')

        if not review_text:
            return jsonify({'status': 'error', 'message': 'No review text provided.'}), 400

        # Step 1: Call the URL Detection function
        url_detection_result = url_detection(review_text)

        if url_detection_result['status'] == 'blocked':
            return jsonify(url_detection_result)

        # Step 2: Call the Review Analysis function
        review_analysis_result = classify_review(review_text)

        if review_analysis_result['status'] == 'rejected':
            log_fake_review(review_text)  # Log the fake review here
            return jsonify({'status': 'rejected', 'message': 'Review classified as fake.'})

        return jsonify({'status': 'accepted', 'message': 'Review classified as real.'})

    except Exception as e:
        print(f"Error in /api/combined_review_analysis: {e}")
        return jsonify({'status': 'error', 'message': 'Internal server error.'}), 500

# New API route to return the fake reviews for the admin dashboard
@app.route('/api/fake_reviews', methods=['GET'])
def get_fake_reviews():
    try:
        fake_reviews = []
        if os.path.exists(FAKE_REVIEW_LOG):
            with open(FAKE_REVIEW_LOG, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    review_text, timestamp = row
                    fake_reviews.append({'text': review_text, 'timestamp': timestamp})

        return jsonify({'status': 'success', 'reviews': fake_reviews})

    except Exception as e:
        print(f"Error in /api/fake_reviews: {e}")
        return jsonify({'status': 'error', 'message': 'Internal server error.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
