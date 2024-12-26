from textblob import TextBlob
from flask import Blueprint, current_app, jsonify, render_template, g
import requests

# Define the blueprint for the app
app = Blueprint('app', __name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/fetch_reviews')
def fetch_reviews():
    # Access the API key from the configuration
    api_key = current_app.config['GOOGLE_PLACES_API_KEY']
    
    # Specify the Place ID of the business
    place_id = 'ChIJj61dQgK6j4AR4GeTYWZsKWw'  # Example: Googleplex Place ID

    # Construct the API request URL
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,rating,reviews&key={api_key}"
    
    # Make the request to Google Places API
    response = requests.get(url)
    data = response.json()

    # Check if the API request was successful
    if data.get('status') != 'OK':
        return jsonify({"error": "Failed to fetch reviews", "details": data}), 500

    # Extract reviews from the API response
    reviews = data['result'].get('reviews', [])
    db = g.db
    cursor = db.cursor()

    # Insert each review into the database
    for review in reviews:
        cursor.execute('''
            INSERT INTO reviews (place_id, author_name, rating, review_text, timestamp, sentiment)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            place_id,
            review.get('author_name'),
            review.get('rating'),
            review.get('text'),
            review.get('time'),
            'pending'  # We'll set sentiment to 'pending' for now and update it after analysis
        ))

    db.commit()

    return jsonify({"message": "Reviews fetched and stored successfully", "num_reviews": len(reviews)})

@app.route('/analyze_sentiment')
def analyze_sentiment():
    db = g.db
    cursor = db.cursor()

    # Retrieve reviews with 'pending' sentiment
    cursor.execute("SELECT id, review_text FROM reviews WHERE sentiment = 'pending'")
    pending_reviews = cursor.fetchall()

    # Analyze sentiment for each pending review
    for review_id, review_text in pending_reviews:
        analysis = TextBlob(review_text)
        
        # Classify sentiment based on polarity score
        if analysis.sentiment.polarity > 0.1:
            sentiment = 'positive'
        elif analysis.sentiment.polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        # Update the review's sentiment in the database
        cursor.execute("UPDATE reviews SET sentiment = ? WHERE id = ?", (sentiment, review_id))

    db.commit()

    return jsonify({"message": "Sentiment analysis completed", "num_analyzed": len(pending_reviews)})

@app.route('/dashboard')
def dashboard():
    # Fetch sentiment data from the database
    db = g.db
    cursor = db.cursor()
    
    cursor.execute("SELECT sentiment, COUNT(*) FROM reviews GROUP BY sentiment")
    sentiment_counts = cursor.fetchall()
    
    # Process sentiment data into chart format
    sentiment_data = {
        "positive": 0,
        "neutral": 0,
        "negative": 0
    }
    for sentiment, count in sentiment_counts:
        if sentiment in sentiment_data:
            sentiment_data[sentiment] = count

    # Fetch recent reviews for display
    cursor.execute("SELECT author_name, review_text, sentiment FROM reviews ORDER BY id DESC LIMIT 5")
    recent_reviews = cursor.fetchall()

    # Render the template with sentiment data and recent reviews
    return render_template('dashboard.html', sentiment_data=sentiment_data, recent_reviews=recent_reviews)