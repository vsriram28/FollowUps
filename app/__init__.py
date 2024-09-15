from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


app = Flask(__name__)

# from app.routes import home,tenants, users, meetings, notes, followups

# app.config['SQLALCHEMY_DATABASE_URI']    = 'postgresql://postgres:your_password@localhost/your_database'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost/sriram'
# app.config.from_object(Config)

db = SQLAlchemy(app)


@app.route('/test')
def test_route():
    return 'This is a test route'


@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404
