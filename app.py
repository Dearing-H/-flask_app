from flask import Flask, render_template, request, flash, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from setup_dp import User, ToDo
from datetime import datetime

app = Flask(__name__)
app.secret_key = "abc123"

#set up the database engine and session
engine = create_engine("sqlite:///todo.db") #replace with your actual DB URI
Session = sessionmaker(bind=engine)
db_session = Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return render_template('sign_up.html')

        # Check if the username already exists
        existing_user = db_session.query(User).filter_by(username=username).first()
        if existing_user:
            flash("Username already exists", "danger")
            return render_template('sign_up.html')

        # hash the password
        hashed_password = generate_password_hash(password)

        # create a new user instance
        new_user = User(username=username, password=hashed_password)

        # add the new user to the database
        db_session.add(new_user)
        db_session.commit()
        flash("You have successfully signed up", "success")
        return redirect(url_for('login'))
    return render_template('sign_up.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        #query the database for the user
        user = db_session.query(User).filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            flash("You have successfully logged in", "success")
            session["user"] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password", "danger")
            return render_template('login.html')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if "user" in session:
        username = session["user"]
        user = db_session.query(User).filter_by(username=username).first()
        todos = user.todos  # Assuming User model has a relationship with Todo model

        return render_template('dashboard.html', todos=todos)
    else:
        flash("You need to login first", "danger")
        return redirect(url_for('login'))

@app.route('/add_task', methods=["POST"])
def add_task():
    if "user" in session:
        task_description = request.form.get("task_description")
        due_date_str = request.form.get("due_date")
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "danger")
            return redirect(url_for('dashboard'))
        
        username = session["user"]
        user = db_session.query(User).filter_by(username=username).first()

        if task_description:
            new_task = ToDo(task=task_description, due_date=due_date, user_id=user.id)
            db_session.add(new_task)
            db_session.commit()
            flash("Task added successfully", "success")
        else:
            flash("Task description cannot be empty", "danger")

        return redirect(url_for('dashboard'))
    else:
        flash("You need to login first", "danger")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop("user", None)
    flash("You have been logged out", "success")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
