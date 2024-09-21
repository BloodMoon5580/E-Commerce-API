# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

CLOUDFLARE_SECRET_KEY = 'YET9pgYpC6i8uSTDMoR-duEqOD8mx6hL8g39RRS0J'

def verify_cloudflare_captcha(response):
    payload = {
        'secret': CLOUDFLARE_SECRET_KEY,
        'response': response
    }
    r = requests.post('https://api.cloudflare.com/client/v4/captcha/verify', json=payload)
    return r.json().get('success')

@app.route('/api/captcha', methods=['POST'])
def verify_captcha():
    data = request.json
    user_input = data.get('user_input')
    captcha_response = data.get('captcha_response')
    
    if verify_cloudflare_captcha(captcha_response):
        # Here, you can add additional verification for user_input if necessary
        return jsonify({'status': 'success', 'message': 'Captcha verified successfully!'})
    else:
        return jsonify({'status': 'failure', 'message': 'Captcha verification failed.'})

if __name__ == '__main__':
    app.run(debug=True)
