from flask import Flask, request, jsonify, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from redis_client import redis_client
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:0808@localhost:5432/url_shortener'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Table
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True)
    clicks = db.Column(db.Integer, default=0)

BASE62 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def encode_base62(num):

    if num == 0:
        return BASE62[0]

    result = []

    while num > 0:
        remainder = num % 62
        result.append(BASE62[remainder])
        num //= 62

    return ''.join(reversed(result))

@app.route('/')
def home():
    return render_template('index.html')

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
            'short_url': request.host_url + existing_url.short_code
        })

    if not long_url:
        return jsonify({'error': 'URL is required'}), 400

    new_url = URL(
        long_url=long_url
    )

    db.session.add(new_url)
    db.session.commit()

    # Generate Base62 short code
    short_code = encode_base62(new_url.id)

    new_url.short_code = short_code

    db.session.commit()

    return jsonify({
        'short_url': request.host_url + short_code
    })
# Redirect to original URL
@app.route('/<short_code>')
def redirect_url(short_code):

    # Check Redis cache first
    cached_url = None

    if redis_client:
        try:
            cached_url = redis_client.get(short_code)
        except:
            pass

    # Always fetch DB row for analytics
    url = URL.query.filter_by(
        short_code=short_code
    ).first()

    if not url:
        return jsonify({
            'error': 'URL not found'
        }), 404

    # Increment clicks
    url.clicks += 1
    db.session.commit()

    # Redis HIT
    if cached_url:
        print("Redis HIT")
        return redirect(cached_url.decode('utf-8'))

    print("Redis MISS")

    # Store in Redis
    if redis_client:
        try:
            redis_client.set(short_code, url.long_url)
        except:
            pass

    return redirect(url.long_url)
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

    port = int(os.environ.get("PORT", 5000))

    app.run(host='0.0.0.0', port=port, debug=False)