import csv
import os
from flask import Flask, jsonify

app = Flask(__name__)

# API endpoint for Fake Reviews

# Path to the fake reviews log file
FAKE_REVIEW_LOG = 'fake_reviews_log.csv'

# API endpoint to read the fake_reviews_log.csv and return the data
@app.route('/api/fake_reviews', methods=['GET'])
def get_fake_reviews():
    try:
        fake_reviews = []

        # Check if the file exists
        if os.path.exists(FAKE_REVIEW_LOG):
            # Open the CSV file and read the reviews
            with open(FAKE_REVIEW_LOG, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 2:  # Ensure the row has the expected format
                        review_text, timestamp = row
                        fake_reviews.append({'text': review_text, 'timestamp': timestamp})

        # Return the fake reviews as JSON
        return jsonify({'status': 'success', 'reviews': fake_reviews})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)