from flask import Flask, render_template, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import user 

app = Flask(__name__)
app.secret_key = "supersecretkey"

#set up the database engine and session
engine = create_engine("sqlite:///your_database.db") #replace with your acutal DB URI
Session = sessionmaker(bind=engine)
db_session = session()

#define user details
username = "Boss"
password =

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

