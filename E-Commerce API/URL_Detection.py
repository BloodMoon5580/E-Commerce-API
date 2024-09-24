import csv
import nltk
nltk.download('punkt')  # Download required libraries

# List of CSV files to load blocked phrases from
csv_files = [
    'Banned Links CSV/BannedLinks_abuse.csv',
    'Banned Links CSV/BannedLinks_adobe.csv',
    'Banned Links CSV/BannedLinks_Ads.csv',
    # Add other CSV files here...
]

# Load blocked phrases from multiple CSV files
blocked_phrases = []
for file_path in csv_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                blocked_phrases.extend(row)  # Extend the list with each phrase in a row
    except FileNotFoundError:
        print(f"Error: CSV file {file_path} not found.")
    except UnicodeDecodeError:
        print(f"Error: Potential encoding issue with CSV file {file_path}. Try specifying encoding.")

# Check if any blocked phrases were loaded
if not blocked_phrases:
    print("Warning: No blocked phrases found in CSV.")

# Function to check if review text contains a blocked phrase
def contains_blocked_phrase(review_text):
    for phrase in blocked_phrases:
        if phrase.lower() in review_text.lower():  # Case-insensitive check
            return True
    return False

# This function is what you'll call from Combined_Review_API.py
def url_detection(review_text):
    if contains_blocked_phrase(review_text):
        return {'status': 'blocked', 'message': 'Review contains a URL. Please remove the URL'}
    else:
        return {'status': 'accepted', 'message': 'Review is accepted.'}
