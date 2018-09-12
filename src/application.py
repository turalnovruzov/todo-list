import config
from flask import Flask, render_template, redirect, request
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

# Initialize the Flask app
app = Flask(__name__)

# Configure the app
app.config.from_object(config.Config())

# Initialize app for db
db = SQLAlchemy(app)


# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'User({self.id}, {self.username})'


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('todos', lazy=True))

    def __repr__(self):
        return f'Todo({self.id}, {self.content}, {self.user_id})'


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""
    # If request method is POST
    if request.method == 'POST':
        # Log the user in
        pass

    # If request method is GET
    else:
        # Render login.html
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Sign user up"""
    # If request method is POST
    if request.method == 'POST':
        # Sign the user up
        pass

    # If request method is GET
    else:
        # Render signup.html
        return render_template('signup.html')
