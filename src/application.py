import config
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Initialize the Flask app
app = Flask(__name__)

# Configure the app
app.config.from_object(config.Config())


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Initialize Session
Session(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""
    # If request method is POST
    if request.method == 'POST':
        # Log the user in
        pass

    # If request method is GET
    else:
        # Render the login.html
        return render_template('login.html')
