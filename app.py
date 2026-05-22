from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Table
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True)
    clicks = db.Column(db.Integer, default=0)

# Generate unique short code
def generate_short_code(length=6):

    characters = string.ascii_letters + string.digits

    while True:
        short_code = ''.join(
            random.choice(characters)
            for _ in range(length)
        )

        # Check if code already exists
        existing_url = URL.query.filter_by(
            short_code=short_code
        ).first()

        if not existing_url:
            return short_code
@app.route('/')
def home():
    return "URL Shortener Running!"

# API to shorten URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()

    long_url = data.get('long_url')
    # Check if URL already exists
    existing_url = URL.query.filter_by(
        long_url=long_url
    ).first()

    if existing_url:
        return jsonify({
            'short_url': f'http://127.0.0.1:5000/{existing_url.short_code}'
        })

    if not long_url:
        return jsonify({'error': 'URL is required'}), 400

    short_code = generate_short_code()

    new_url = URL(
        long_url=long_url,
        short_code=short_code
    )

    db.session.add(new_url)
    db.session.commit()

    return jsonify({
        'short_url': f'http://127.0.0.1:5000/{short_code}'
    })
# Redirect to original URL
@app.route('/<short_code>')
def redirect_url(short_code):

    url = URL.query.filter_by(
        short_code=short_code
    ).first()

    if url:

        # Increase click count
        url.clicks += 1
        db.session.commit()

        return redirect(url.long_url)

    return jsonify({'error': 'URL not found'}), 404

# Analytics API
@app.route('/stats/<short_code>')
def get_stats(short_code):

    url = URL.query.filter_by(
        short_code=short_code
    ).first()

    if not url:
        return jsonify({
            'error': 'URL not found'
        }), 404

    return jsonify({
        'long_url': url.long_url,
        'short_code': url.short_code,
        'clicks': url.clicks
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)