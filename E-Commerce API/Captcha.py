# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

CLOUDFLARE_SECRET_KEY = '0x4AAAAAAAkaNGmDfYiXue1PgB1ZUX5DEv8'

def verify_cloudflare_captcha(captcha_response):
    """Verify the Turnstile CAPTCHA response with Cloudflare API."""
    payload = {
        'secret': CLOUDFLARE_SECRET_KEY,
        'response': captcha_response
    }
    try:
        response = requests.post('https://challenges.cloudflare.com/turnstile/v0/siteverify', json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json().get('success', False)
    except requests.RequestException as e:
        app.logger.error(f'Error verifying CAPTCHA: {e}')
        return False

@app.route('/api/captcha', methods=['POST'])
def verify_captcha():
    """Endpoint to verify CAPTCHA and user input."""
    data = request.get_json()
    user_input = data.get('user_input')
    captcha_response = data.get('captcha_response')
    
    if not user_input or not captcha_response:
        return jsonify({'status': 'failure', 'message': 'Missing user input or CAPTCHA response.'}), 400
    
    if verify_cloudflare_captcha(captcha_response):
        # Additional verification for user_input can be added here
        return jsonify({'status': 'success', 'message': 'CAPTCHA verified successfully!'})
    else:
        return jsonify({'status': 'failure', 'message': 'CAPTCHA verification failed.'}), 403

if __name__ == '__main__':
    app.run(debug=True)
