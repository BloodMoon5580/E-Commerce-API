import pickle
import re
import nltk
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
nltk.download('punkt')

# Define the text_process function for preprocessing
def text_process(text):
    """
    Preprocess the input text:
    - Convert to lowercase
    - Remove punctuation
    - Tokenize using nltk
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = nltk.word_tokenize(text)
    return ' '.join(tokens)

# Load the saved SVM model and vectorizer
try:
    with open('E-Commerce API/Comment Reviewer/Deep Learning/Models/dnn_model1.pkl', 'rb') as model_file:
        loaded_svm_model = pickle.load(model_file)

    with open('E-Commerce API/Comment Reviewer/Deep Learning/Models/dnn_vectorizer1.pkl', 'rb') as vectorizer_file:
        tfidf_vectorizer = pickle.load(vectorizer_file)

except Exception as e:
    print(f"Error loading SVM model or vectorizer: {e}")

# Load the saved DNN model
try:
    loaded_dnn_model = load_model('E-Commerce API/Comment Reviewer/Deep Learning/Models/dnn_model.h5')
except Exception as e:
    print(f"Error loading DNN model: {e}")

# This function is what you'll call from Combined_Review_API.py
def classify_review(review_text, model_type='svm'):
    """
    Classify the review text using either 'svm' or 'dnn' model.
    """
    try:
        # Preprocess the review text
        preprocessed_comment = text_process(review_text)

        # Use the loaded vectorizer to transform the preprocessed text
        transformed_comment = tfidf_vectorizer.transform([preprocessed_comment])

        # Convert sparse matrix to dense array
        transformed_comment_dense = transformed_comment.toarray()

        # Choose the model based on the model_type parameter
        if model_type == 'svm':
            prediction = loaded_svm_model.predict(transformed_comment_dense)[0]
        elif model_type == 'dnn':
            # DNN expects the input in dense array form
            prediction = (loaded_dnn_model.predict(transformed_comment_dense) > 0.5).astype(int)[0][0]
        else:
            return {'status': 'error', 'message': 'Invalid model type specified.'}

        # Interpret the prediction and return the appropriate message
        if prediction == 0:  # Assuming '0' means fake
            return {'status': 'rejected', 'message': 'Review classified as fake.'}
        else:
            return {'status': 'accepted', 'message': 'Review not classified as fake.'}

    except Exception as e:
        print(f"Error during classification: {e}")
        return {'status': 'error', 'message': 'Classification error.'}
