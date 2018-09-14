import config
from flask import Flask, render_template, redirect, request, make_response, flash, jsonify
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

# Initialize the Flask app
app = Flask(__name__)

# Configure the app
app.config.from_object(config.Config())

# Initialize database
db = SQLAlchemy(app)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'User({self.id}, {self.username})'


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('todos', lazy=True))

    def __repr__(self):
        return f'Todo({self.id}, {self.content}, {self.user_id})'


# User loader for login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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

    # Check if there is a logged in user
    if current_user.is_authenticated:
        return redirect('/')

    # If request method is POST
    if request.method == 'POST':

        # Ensure username is provided
        if not request.form.get('username'):
            return make_response(('Username required', 400))

        # Ensure password is provided
        if not request.form.get('password'):
            return make_response(('Password required', 400))

        # Query database for user with the username
        user = User.query.filter_by(username=request.form.get('username')).first()

        # Check username exists and passwords match, if not flash error message and redirect to /login
        if not user or not check_password_hash(user.password, request.form.get('password')):
            flash('Username or password wrong', 'danger')
            return redirect('/login')

        # Get remember me
        remember = request.form.get('remember') if request.form.get('remember') else False

        # Log the user in
        login_user(user, remember)

        # Redirect to /
        return redirect('/')

    # If request method is GET
    else:
        # Render login.html
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Sign user up"""

    # Check if there is a logged in user
    if current_user.is_authenticated:
        return redirect('/')

    # If request method is POST
    if request.method == 'POST':
        # Ensure username exists
        if not request.form.get('username'):
            return make_response(('Username required', 400))

        # Ensure password exists
        if not request.form.get('password'):
            return make_response(('Password required', 400))

        # Ensure confirmation exists
        if not request.form.get('confirmation'):
            return make_response(('Confirmation required', 400))

        # Check if passwords match
        if request.form.get('password') != request.form.get('confirmation'):
            return make_response(('Passwords don\'t match', 400))

        # Check if username is already taken
        if User.query.filter_by(username=request.form.get('username')).first():
            return make_response(('Username is already taken.', 400))

        # Create the User
        user = User(request.form.get('username'),
                    generate_password_hash(request.form.get('password')))

        # Insert the user to database
        db.session.add(user)
        db.session.commit()

        # Get remember me value
        remember = request.form.get('remember') if request.form.get('remember') else False

        # Log the user in
        login_user(user, remember)

        # Flash message
        flash('Signed you up!', 'success')

        # Redirect to /
        return redirect('/signup')

    # If request method is GET
    else:
        # Render signup.html
        return render_template('signup.html')


@app.route('/username_check', methods=['POST'])
def username_check():
    """
    Checks if username is already taken

    Response:
    Json data containing username: string, and exists: boolean
    """

    # Ensure username is provided
    if not request.form.get('username'):
        return make_response(('Username required', 400))

    # Create the result object
    result = {
        'username': request.form.get('username')
    }

    # Check database for username
    result['exists'] = True if User.query.filter_by(username=result['username']).first() else False

    # Return json
    return jsonify(result)


@app.route('/logout')
def logout():
    """Logs the user out"""

    # Log the user out
    logout_user()

    # Redirect to login page
    return redirect('/login')
