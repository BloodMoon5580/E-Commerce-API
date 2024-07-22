# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

RECAPTCHA_SECRET_KEY = 'YOUR_SECRET_KEY'

def verify_recaptcha(response):
    payload = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    return r.json().get('success')

@app.route('/api/verify', methods=['POST'])
def verify_captcha():
    data = request.json
    user_input = data.get('user_input')
    recaptcha_response = data.get('recaptcha_response')
    
    if verify_recaptcha(recaptcha_response):
        # Here, you can add additional verification for user_input if necessary
        return jsonify({'status': 'success', 'message': 'Captcha verified successfully!'})
    else:
        return jsonify({'status': 'failure', 'message': 'Captcha verification failed.'})

if __name__ == '__main__':
    app.run(debug=True)
