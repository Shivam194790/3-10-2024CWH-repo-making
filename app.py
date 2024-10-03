from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
socketio = SocketIO(app)

# Configuration for SQLAlchemy and MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/user'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Create a model for the User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

# Create the tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# Route for the registration form
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            return "Passwords do not match!"

        # Create a new user object
        new_user = User(name=name, email=email, password=password)

        # Add the user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('register_success'))
        except:
            db.session.rollback()
            return "Error: Email already exists."

    return render_template('register.html')

# Route for successful registration
@app.route('/register-success')
def register_success():
    return "Registration successful!"


# Route for the login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            return redirect(url_for('login_success'))
        else:
            return "Invalid email or password"

    return render_template('login.html')

# Route for successful login
@app.route('/login-success')
def login_success():
    return "Login successful!"




@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/networking')
def networking():
    return render_template('networking.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/events')
def events():
    return render_template('events.html')

if __name__ == '__main__':
    # socketio.run(app)
    socketio.run(app, debug=True)
#change 