import random
import string

def generate_short_code(URL, length=6):

    characters = string.ascii_letters + string.digits

    while True:

        short_code = ''.join(
            random.choice(characters)
            for _ in range(length)
        )

        existing_url = URL.query.filter_by(
            short_code=short_code
        ).first()

        if not existing_url:
            return short_code