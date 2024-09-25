from flask import Flask, jsonify, request
from flask_cors import CORS
from URL_Detection import url_detection  # Import the URL Detection module
from Review_Analysis import classify_review  # Import the Review Analysis module
import csv
from datetime import datetime

app = Flask(__name__)
CORS(app)

FAKE_REVIEW_LOG = 'E-Commerce API/fake_reviews_log.csv'

# Log the fake review to a CSV file
def log_fake_review(review_text):
    with open(FAKE_REVIEW_LOG, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write the review text and current timestamp
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

if __name__ == '__main__':
    app.run(debug=True)