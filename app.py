from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import os

app = Flask(__name__)

# ------------------ DATABASE CONFIG ------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

# ✅ SECRET_KEY from environment variable (fallback to defaultsecret)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'defaultsecret')

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ------------------ LOAD ML MODEL ------------------
vectorizer, model = pickle.load(open('model.pkl', 'rb'))

# ------------------ USER MODEL ------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))  # hashed password
    role = db.Column(db.String(50))       # "admin" or "user"

# ------------------ POST MODEL ------------------
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.Text)
    result = db.Column(db.String(50))  # "Cyberbullying detected" or "Safe content"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------ HOME PAGE ------------------
@app.route('/')
def home():
    return render_template('home.html')

# ------------------ ABOUT PAGE ------------------
@app.route('/about')
def about():
    return render_template('about.html')

# ------------------ SIGNUP PAGE ------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists. Please choose another."

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        print("User saved:", new_user.id, new_user.username, new_user.role)  # ✅ Debug print
        
        # ✅ Flash message after signup
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

# ------------------ LOGIN PAGE ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            return "Invalid username or password."

    return render_template('login.html')

# ------------------ USER DASHBOARD ------------------
@app.route('/user_dashboard', methods=['GET', 'POST'])
@login_required
def user_dashboard():
    result = None
    if request.method == 'POST':
        text = request.form['post']
        prediction = model.predict(vectorizer.transform([text]))
        result = "Cyberbullying detected" if prediction[0] == 1 else "Safe content"

        # ✅ Save post and result to DB
        new_post = Post(user_id=current_user.id, text=text, result=result)
        db.session.add(new_post)
        db.session.commit()
        print("Post saved:", new_post.id, new_post.text, new_post.result)  # ✅ Debug print

    return render_template('user_dashboard.html', result=result)

# ------------------ ADMIN DASHBOARD ------------------
@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    flagged_posts = Post.query.filter_by(result="Cyberbullying detected").all()
    return render_template('admin_dashboard.html', flagged_posts=flagged_posts)

# ------------------ LOGOUT ------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully!", "success")
    return redirect(url_for('login'))

# Ensure tables exist before running
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

