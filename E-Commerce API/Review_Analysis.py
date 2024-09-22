from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
import re
import nltk
nltk.download('punkt')  # Download the NLTK data for tokenization

# Define the text_process function for preprocessing
def text_process(text):
    """
    Preprocess the input text:
    - Convert to lowercase
    - Remove punctuation
    - Tokenize using nltk
    """
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    tokens = nltk.word_tokenize(text)  # Tokenize the text into words
    return ' '.join(tokens)  # Return processed text as a string

# Load the saved model and vectorizer
try:
    with open('E-Commerce API/Comment Reviewer/model.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)

    with open('E-Commerce API/Comment Reviewer/vectorizer.pkl', 'rb') as vectorizer_file:
        tfidf_vectorizer = pickle.load(vectorizer_file)

except Exception as e:
    print(f"Error loading model or vectorizer: {e}")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Function to classify reviews using the loaded model
def classify_review(text):
    try:
        # Preprocess the review text
        preprocessed_comment = text_process(text)

        # Use the loaded vectorizer to transform the preprocessed text
        transformed_comment = tfidf_vectorizer.transform([preprocessed_comment])

        # Use the loaded model to predict if the review is fake or not
        prediction = loaded_model.predict(transformed_comment)[0]

        return prediction
    except Exception as e:
        print(f"Error during classification: {e}")
        return "Error"

# API route for review analysis
@app.route('/api/review_analysis', methods=['POST'])
def review_analysis():
    try:
        # Get the review text from the POST request
        data = request.json
        review_text = data.get('review_text')

        if not review_text:
            return jsonify({'status': 'error', 'message': 'No review text provided.'}), 400

        # Classify the review using the model
        review_class = classify_review(review_text)

        if review_class == "Error":
            return jsonify({'status': 'error', 'message': 'Classification error.'}), 500

        # Return the result based on the classification
        if review_class == 0:  # Assuming '0' means fake review (trained solely on fake reviews)
            return jsonify({'status': 'rejected', 'message': 'Review classified as fake.'})
        else:  # Assuming '1' means not fake
            return jsonify({'status': 'accepted', 'message': 'Review not classified as fake.'})

    except Exception as e:
        print(f"Error in /api/review_analysis: {e}")
        return jsonify({'status': 'error', 'message': 'Internal server error.'}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
    
    
