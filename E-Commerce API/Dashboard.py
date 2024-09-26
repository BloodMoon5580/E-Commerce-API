from flask import Flask, render_template
from flask_cors import CORS
import Combined_Review_API  # Import your Combined_Review_API

app = Flask(__name__)
CORS(app)  # Enable CORS globally for all routes

@app.route('/api/dashboard')
def admin_dashboard():
    # Fetch daily fake review counts from Combined_Review_API
    daily_counts = Combined_Review_API.get_daily_fake_review_counts()

    # Convert the data into a format that can be rendered as an HTML table
    review_data = [{'date': date, 'count': count} for date, count in daily_counts.items()]

    # Render the HTML template and pass the data
    return render_template('E-Commerce API/Templates/Dashboard.html', review_data=review_data)

if __name__ == '__main__':
    app.run()
