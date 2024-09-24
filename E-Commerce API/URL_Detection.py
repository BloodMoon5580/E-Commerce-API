import re
import csv
import nltk
nltk.download('punkt')  # Download required libraries

# Regular expressions to detect common URL formats and protocols
url_patterns = [
    r'\b(?:https?|ftp|ftps|sftp|smtp|imap|pop3|telnet|ssh|ldap|ldaps|dns|ws|wss|rtp|rtsp|smb|nfs|mailto|urn|urn:isbn:|git|bittorrent)://\S+',  # Match URLs starting with http, https, ftp, imap, pop3, telnet, ssh, ldap
    r'\b(?:www\.)\S+',  # Match URLs starting with www.
    r'\b\S+\.(?:com|net|org|io|gov|edu|co|biz|info|me|tech)\b',  # Match common domain extensions (.com, .net, etc.)
    r'\b\S+\s*\{dot\}\s*\S+\b',  # Match [dot] patterns like google{dot}com
    r'\b\S+\s*\[dot\]\s*\S+\b',  # Match [dot] patterns like google[dot]com
    r'\b\S+\s*\(dot\)\s*\S+\b',  # Match (dot) patterns like google(dot)com
    r'\b\S+\s*dot\s*\S+\b'  # Match dot patterns like google dot com
]


# List of CSV files to load blocked phrases from
csv_files = [
    'E-Commerce API/Banned Links CSV/BannedLinks_Abuse.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Adobe.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Ads.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Basic.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_crypto.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_drugs.csv',
    'E-Commerce API/Banned Links CSV/BannedLinks_Everything.csv',
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

blocked_phrases = []
for file_path in csv_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                blocked_phrases.extend(row)
    except FileNotFoundError:
        print(f"Error: CSV file {file_path} not found.")
    except UnicodeDecodeError:
        print(f"Error: Potential encoding issue with CSV file {file_path}. Try specifying encoding.")

# Function to check if review text contains a blocked URL
def contains_blocked_url(text):
    print(f"Checking text for URL patterns: {text}")  # Debugging
    # Check for URL patterns using regex
    for pattern in url_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

# This function is what you'll call from Combined_Review_API.py
def url_detection(review_text):
    if contains_blocked_url(review_text):
        return {'status': 'blocked', 'message': 'Review contains a URL. Please remove the URL'}
    else:
        return {'status': 'accepted', 'message': 'Review is accepted.'}
