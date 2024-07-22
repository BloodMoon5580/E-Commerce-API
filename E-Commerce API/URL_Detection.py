# URL_Detection.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import re
import nltk
nltk.download('punkt')

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Enable CORS for all routes under /api/*

# URL detection using heuristic analysis
def contains_url(text):
    url_pattern = re.compile(r"https?://\S+|www\.\S+")
    if url_pattern.search(text):
        return True
    return False

@app.route('/api/url_detection', methods=['POST'])
def url_detection():
    data = request.json
    review_text = data.get('review_text')

    if contains_url(review_text):
        return jsonify({'status': 'blocked', 'message': 'Review contains a URL and is blocked.'})
    else:
        return jsonify({'status': 'accepted', 'message': 'Review is accepted.'})

if __name__ == '__main__':
    app.run(debug=True)
