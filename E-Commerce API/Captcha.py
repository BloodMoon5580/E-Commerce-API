# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

CLOUDFLARE_SECRET_KEY = 'YOUR_CLOUDFLARE_SECRET_KEY'

def verify_cloudflare_captcha(captcha_response):
    payload = {
        'secret': CLOUDFLARE_SECRET_KEY,
        'response': captcha_response
    }
    try:
        r = requests.post('https://api.cloudflare.com/client/v4/captcha/verify', json=payload)
        r.raise_for_status()  # Raise an error for bad responses
        return r.json().get('success', False)
    except requests.exceptions.RequestException as e:
        print(f"Error verifying CAPTCHA: {e}")
        return False

@app.route('/api/captcha', methods=['POST'])
def verify_captcha():
    data = request.json
    user_input = data.get('user_input')
    captcha_response = data.get('captcha_response')
    
    if verify_cloudflare_captcha(captcha_response):
        # Additional user input verification can be done here if needed
        return jsonify({'status': 'success', 'message': 'Captcha verified successfully!'})
    else:
        return jsonify({'status': 'failure', 'message': 'Captcha verification failed.'})

if __name__ == '__main__':
    app.run(debug=True)
