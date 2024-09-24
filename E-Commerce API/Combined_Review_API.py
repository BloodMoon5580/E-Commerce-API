from flask import Flask, jsonify, request
from flask_cors import CORS

# Now, import the modules
from URL_Detection import url_detection  # Import the URL Detection module
from Review_Analysis import classify_review  # Import the Review Analysis module

app = Flask(__name__)
CORS(app)

# API route to handle combined review and URL analysis
@app.route('/api/combined_review_analysis', methods=['POST'])
def combined_review_analysis():
    try:
        data = request.json
        review_text = data.get('review_text')

        if not review_text:
            return jsonify({'status': 'error', 'message': 'No review text provided.'}), 400

        # Step 1: Call the URL Detection function
        url_detection_result = url_detection(review_text)

        if url_detection_result['status'] == 'blocked':
            # Return the message from URL detection
            return jsonify({
                'status': 'blocked',
                'message': url_detection_result['message']  # Top-level message from URL detection
            })

        # Step 2: If no blocked URL, call the Review Analysis function
        review_analysis_result = classify_review(review_text)

        # Combine results into a single response with a top-level message
        return jsonify({
            'status': review_analysis_result['status'],
            'message': review_analysis_result['message']  # Top-level message from review analysis
        })

    except Exception as e:
        print(f"Error in /api/combined_review_analysis: {e}")
        return jsonify({'status': 'error', 'message': 'Internal server error.'}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)  # Running on port 5000