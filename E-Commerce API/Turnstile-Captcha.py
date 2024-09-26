import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Your Cloudflare secret key
SECRET_KEY = 'your_secret_key_here'

# Route for the login form
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    captcha_response = request.form.get('cf-turnstile-response')  # Captcha response token

    if not captcha_response:
        return jsonify({'error': 'CAPTCHA not completed'}), 400

    # Validate CAPTCHA
    captcha_validation = validate_captcha(captcha_response)
    if not captcha_validation['success']:
        return jsonify({'error': 'CAPTCHA validation failed'}), 400

    # Proceed with your login logic
    # For example, authenticate username and password here
    return jsonify({'message': 'Login successful'})


def validate_captcha(captcha_response):
    """Send a request to Cloudflare Turnstile to validate the CAPTCHA"""
    url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
    payload = {
        'secret': SECRET_KEY,
        'response': captcha_response
    }
    response = requests.post(url, data=payload)
    return response.json()


if __name__ == '__main__':
    app.run(debug=True)
