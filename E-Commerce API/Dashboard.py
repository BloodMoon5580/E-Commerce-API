from flask import Flask, render_template, jsonify
import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Path to the CSV file where fake reviews are logged
FAKE_REVIEW_LOG = 'E-Commerce API/fake_reviews_log.csv'

# Helper function to get daily fake review counts
def get_daily_fake_review_counts():
    daily_fake_reviews = defaultdict(int)

    try:
        with open(FAKE_REVIEW_LOG, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                date = row[1][:10]  # Extract the date part (YYYY-MM-DD)
                daily_fake_reviews[date] += 1
    except FileNotFoundError:
        return [], []

    # Sort dates and get the counts
    sorted_dates = sorted(daily_fake_reviews.keys())
    counts = [daily_fake_reviews[date] for date in sorted_dates]
    return sorted_dates, counts

# Route to render the admin dashboard with the chart
@app.route('/dashboard')
def render_dashboard():
    dates, counts = get_daily_fake_review_counts()

    if not dates:
        return "No fake reviews to display."

    return render_template('E-Commerce API/Templates/Admin.html', chart_data={'dates': dates, 'counts': counts})

# API route to get the list of fake reviews
@app.route('/api/fake_reviews')
def get_fake_reviews():
    reviews = []
    try:
        with open(FAKE_REVIEW_LOG, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                reviews.append({'text': row[0], 'timestamp': row[1]})
    except FileNotFoundError:
        return jsonify({'reviews': []})

    return jsonify({'reviews': reviews})

if __name__ == '__main__':
    app.run(debug=True)