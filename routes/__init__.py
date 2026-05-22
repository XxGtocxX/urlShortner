from flask import request, jsonify, redirect
from models import db, URL
from utils import generate_short_code
from redis_client import redis_client


def register_routes(app):

    @app.route('/')
    def home():
        return "URL Shortener Running!"

    @app.route('/shorten', methods=['POST'])
    def shorten_url():

        data = request.get_json()

        long_url = data.get('long_url')

        if not long_url:
            return jsonify({
                'error': 'URL is required'
            }), 400

        # Check existing URL
        existing_url = URL.query.filter_by(
            long_url=long_url
        ).first()

        if existing_url:
            return jsonify({
                'short_url': request.host_url + existing_url.short_code
            })
        short_code = generate_short_code(URL)

        new_url = URL(
            long_url=long_url,
            short_code=short_code
        )

        db.session.add(new_url)
        db.session.commit()

        return jsonify({
            'short_url': request.host_url + short_code
        })

    @app.route('/<short_code>')
    def redirect_url(short_code):

        # Check Redis cache first
        cached_url = redis_client.get(short_code)

        # Always fetch DB for analytics
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
            return redirect(cached_url.decode('utf-8'))

        # Redis MISS
        redis_client.set(short_code, url.long_url)

        return redirect(url.long_url)

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