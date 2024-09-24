import pickle
import re
import nltk
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

# Load the saved model and vectorizer
try:
    with open('E-Commerce API/Comment Reviewer/svm_model.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)

    with open('E-Commerce API/Comment Reviewer/svm_vectorizer.pkl', 'rb') as vectorizer_file:
        tfidf_vectorizer = pickle.load(vectorizer_file)

except Exception as e:
    print(f"Error loading model or vectorizer: {e}")

# This function is what you'll call from Combined_Review_API.py
def classify_review(review_text):
    try:
        # Preprocess the review text
        preprocessed_comment = text_process(review_text)

        # Use the loaded vectorizer to transform the preprocessed text
        transformed_comment = tfidf_vectorizer.transform([preprocessed_comment])

        # Convert sparse matrix to dense array (needed for SVC)
        transformed_comment_dense = transformed_comment.toarray()

        # Use the loaded model to predict if the review is fake or not
        prediction = loaded_model.predict(transformed_comment_dense)[0]

        if prediction == 0:  # Assuming '0' means fake
            return {'status': 'rejected', 'message': 'Review classified as fake.'}
        else:
            return {'status': 'accepted', 'message': 'Review not classified as fake.'}
    except Exception as e:
        print(f"Error during classification: {e}")
        return {'status': 'error', 'message': 'Classification error.'}
