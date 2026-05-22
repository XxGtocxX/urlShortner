from flask import Flask
from models import db
from routes import register_routes

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

register_routes(app)

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)