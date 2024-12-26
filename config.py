import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    GOOGLE_PLACES_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY') or 'AIzaSyB77ipo324Qu_ls5OJ6CgyEfksxgOf8N7s'
    DATABASE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'reviews.db')
