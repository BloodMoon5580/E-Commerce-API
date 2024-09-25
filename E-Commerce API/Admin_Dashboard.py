from flask import Flask, render_template, request, jsonify
import csv
from collections import defaultdict

app = Flask(__name__)

# Data storage (temporary, consider database integration)
FAKE_REVIEW_LOG = 'E-Commerce API/fake_reviews_log.csv'
fake_review_counts = defaultdict(int)  # Dictionary to store daily fake review counts

# Helper function to update fake review counts from CSV
def update_fake_review_counts():
    global fake_review_counts
    fake_review_counts.clear()  # Clear existing data

    try:
        with open(FAKE_REVIEW_LOG, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                date = row[1][:10]  # Extract the date part (YYYY-MM-DD)
                fake_review_counts[date] += 1
    except FileNotFoundError:
        pass  # Ignore if the log file doesn't exist

# Route to render the dashboard with chart data
@app.route('/dashboard')
def render_dashboard():
    update_fake_review_counts()  # Update data before rendering the template

    dates = list(fake_review_counts.keys())
    counts = list(fake_review_counts.values())

    return render_template('dashboard.html', chart_data={'dates': dates, 'counts': counts})

# ... other notification handling routes from your original code ...

if __name__ == '__main__':
    app.run(debug=True)