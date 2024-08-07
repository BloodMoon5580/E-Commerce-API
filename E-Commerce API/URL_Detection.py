from flask import Flask, jsonify, request
from flask_cors import CORS
import csv
import nltk
nltk.download('punkt')  # Download required libraries

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Enable CORS for all routes under /api/*

# Load blocked phrases from CSV file, handle potential encoding issues
blocked_phrases = []
try:
    with open('URL_Pattern.csv', 'r', encoding='utf-8') as csvfile:  # Specify encoding (optional)
        reader = csv.reader(csvfile)
        for row in reader:
            blocked_phrases.extend(row)  # Extend the list with each phrase in a row
except FileNotFoundError:
    print("Error: CSV file not found.")
except UnicodeDecodeError:
    print("Error: Potential encoding issue with CSV file. Try specifying encoding.")

# Check if any blocked phrases were loaded
if not blocked_phrases:
    print("Warning: No blocked phrases found in CSV.")



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
        return jsonify({'status': 'blocked', 'message': 'Review contains a URL. Please remove the URL'})
    else:
        return jsonify({'status': 'accepted', 'message': 'Review is accepted.'})
    
    # ... (existing code for reading CSV)
    if not blocked_phrases:
        print("Warning: No blocked phrases found in CSV.")


if __name__ == '__main__':
    app.run(debug=True)
