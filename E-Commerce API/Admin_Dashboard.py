from flask import Flask, request, jsonify

app = Flask(__name__)

# API endpoint for failed CAPTCHA login attempts
@app.route('/api/notifications/loginFailures', methods=['POST'])
def login_failures():
    data = request.get_json()
    
    username = data.get('username')
    failed_attempts = data.get('failedAttempts')
    ip_address = data.get('ipAddress')

    if username and failed_attempts >= 3 and ip_address:
        # Notify admin logic can go here
        return jsonify({"message": "Admin notified of login failures."}), 200
    else:
        return jsonify({"error": "Invalid data provided."}), 400

 
# API endpoint for defamatory reviews
@app.route('/api/notifications/defamatoryReview', methods=['POST'])
def defamatory_review():
    data = request.get_json()

    user_id = data.get('userId')
    product_id = data.get('productId')
    review_text = data.get('reviewText')

    if user_id and product_id and "defamatory" in review_text.lower():
        # Notify admin logic can go here
        return jsonify({"message": "Admin notified of defamatory review."}), 200
    else:
        return jsonify({"error": "Invalid data provided."}), 400

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)