import config
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Initialize the Flask app
app = Flask(__name__)

# Configure the app
app.config.from_object(config.Config())

# Initialize Session
Session(app)
