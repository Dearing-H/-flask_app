from flask import Flask, render_template, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User
app = Flask(__name__)
app.secret_key = "supersecretkey"

#set up the database engine and session
engine = create_engine("sqlite:///your_database.db") #replace with your acutal DB URI
Session = sessionmaker(bind=engine)
db_session = session()

#define user details
username = "Boss"
password = "Bstream1"

#hash` the password
hashed_password = generate_password_hash(password)

#create a new user instance
new_user = User(username=username, password=hashed_password)

#add the new user to the database
db_session.add(new_user)
db_session.commit()
print("User added to the database")

@app.route('/')
def home():
    return render_template('index.html')

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
            return render_template('index.html')
        else:
            flash("Invalid username or password", "danger")
            return render_template('login.html')
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

