# URL_Detection.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import csv
import nltk
nltk.download('punkt')  # Download required libraries

app = Flask(_name_)
CORS(app, resources={r"/api/*": {"origins": ""}})  # Enable CORS for all routes under /api/

# Load blocked phrases from CSV file
blocked_phrases = []
with open('CSV-File-Goes-Here', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        blocked_phrases.extend(row)  # Extend the list with each phrase in a row

# Function to check if review text contains a blocked phrase
def contains_blocked_phrase(text):
    for phrase in blocked_phrases:
        if phrase.lower() in text.lower():  # Case-insensitive check
            return True
    return False

@app.route('/api/url_detection', methods=['POST'])
def url_detection():
    data = request.json
    review_text = data.get('review_text')

    if contains_blocked_phrase(review_text):
        return jsonify({'status': 'blocked', 'message': 'Review contains a blocked phrase.'})
    elif contains_url(review_text):  # Check for URLs even if no blocked phrases
        return jsonify({'status': 'blocked', 'message': 'Review contains a URL and is blocked.'})
    else:
        return jsonify({'status': 'accepted', 'message': 'Review is accepted.'})

# URL detection (unchanged)
def contains_url(text):
    url_pattern = re.compile(r"https?://\S+|www\.\S+")
    if url_pattern.search(text):
        return True
    return False

if _name_ == '_main_':
    app.run(debug=True)

