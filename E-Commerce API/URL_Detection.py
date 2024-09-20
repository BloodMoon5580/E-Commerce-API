from flask import Flask, jsonify, request
from flask_cors import CORS
import csv
import nltk
nltk.download('punkt'); # Download required libraries

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}); # Enable CORS for all routes under /api/*

# List of CSV files to load blocked phrases from
csv_files = [
    'Banned Links CSV/BannedLinks_abuse.csv',
    'Banned Links CSV/BannedLinks_adobe.csv',
    'Banned Links CSV/BannedLinks_Ads.csv',
    'Banned Links CSV/BannedLinks_basic.csv',
    'Banned Links CSV/BannedLinks_crypto.csv',
    'Banned Links CSV/BannedLinks_drugs.csv',
    'Banned Links CSV/BannedLinks_everything.csv',
    'Banned Links CSV/BannedLinks_Facebook.csv',
    'Banned Links CSV/BannedLinks_Fraud.csv'
]

# Load blocked phrases from multiple CSV files
blocked_phrases = []
for file_path in csv_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                blocked_phrases.extend(row); # Extend the list with each phrase in a row
    except FileNotFoundError:
        print(f"Error: CSV file {file_path} not found.")
    except UnicodeDecodeError:
        print(f"Error: Potential encoding issue with CSV file {file_path}. Try specifying encoding.")

# Check if any blocked phrases were loaded
if not blocked_phrases:
    print("Warning: No blocked phrases found in CSV.")

# Function to check if review text contains a blocked phrase
def contains_blocked_phrase(text):
    for phrase in blocked_phrases:
        if phrase.lower() in text.lower(): # Case-insensitive check
            return True
    return False

@app.route('/api/url_detection', methods=['POST'])
def url_detection():
    data = request.json
    review_text = data.get('review_text')

    if contains_blocked_phrase(review_text):
        return jsonify({'status': 'blocked', 'message': 'Review contains a URL. Please remove the URL'})
    else:
        return jsonify({'status': 'accepted', 'message': 'Review is accepted.'})

if __name__ == '__main__':
    app.run(debug=True)