import csv
import nltk
nltk.download('punkt')  # Download required libraries

# List of CSV files to load blocked phrases from
csv_files = [
    'E-Commerce API/Banned Links CSV/BannedLinks_abuse.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_adobe.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Ads.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_basic.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_crypto.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_drugs.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_everything.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Facebook.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Fraud.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Gambling.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Malware.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Phishing.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Piracy.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Porn.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Ransomware.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Redirect.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Scam.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Smart-TV.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_TikTok.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Torrent.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Tracking.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Twitter.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Youtube.csv',
    'E-Commerce API/Banned Links CSV/Url_pattern.csv'
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
