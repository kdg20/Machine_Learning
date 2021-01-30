from flask import Flask,render_template,jsonify,request,url_for,redirect,session
from flask_pymongo import PyMongo #import PyMongo
from flask_mongoengine import MongoEngine
import json
import os
import sys
from pymongo import MongoClient #import Mongo Client
from bson.json_util import dumps #used to convert bson into json
from bson.objectid import ObjectId # used to generate random ids
from werkzeug.security import generate_password_hash,check_password_hash
from bson import json_util
from flask.helpers import flash

TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('static')

app = Flask(__name__)
app.secret_key = "secretkey"
#Mongo connectivity
app.config['MONGO_URI'] = "mongodb://localhost:27017/E_Learning_System" 
mongo = PyMongo(app)

mongo_client = MongoClient('mongodb://localhost:27017')
db = mongo_client.E_Learning_System
user_data = db.get_collection('login_details')

#This route the page to the home page 
@app.route('/')
def hello_world():
   return render_template('home.html')

#this is success page route
@app.route('/success')
def success():
   return "Logged in !"



#Route to the login page of the user
@app.route('/login', methods=['POST','GET'])
def login():
   if request.method=='POST':
      #get the user input mail id 
      user_email = request.form.get("inputEmail")
      #get the user input password
      user_password = request.form.get("inputPassword")
      #get the user object which have Email equal to user input email
      #and password
      user = user_data.find_one({},{'Email' : user_email,'userName':1,'Password':1})
      email = user.get('Email')
      user_name = user.get('userName')
      #check users mail id and password 
      #if correct then redirect to the dashboard
      #else redirect to the loging page with error message
      if email == user_email and check_password_hash(user.get('Password'),user_password):
         #return render_template('index.html',username=user_name,user=user)
         session['username']=user_name
         return redirect(url_for('index',username=user_name))
      else:
         #Invalid login credentials
         #redirect again to the login page and show error message
         return render_template('auth/login.html',error_message="Invalid Credentials!")
   return render_template('auth/login.html')

#this is home page
#when user visit the site this comes first
@app.route('/home')
def home():
      if 'username' in session:
         user_details = user_data.find_one({'userName':session['username']})
         username = user_details.get('userName')
         name = user_details.get('fullName')
         return render_template('home.html',username=username,name=name)
      return render_template('home.html')


@app.route('/index/<username>')
def index(username):
   user_details = user_data.find_one({'userName':username})
   user_name = user_details.get('userName')
   email_id = user_details.get('Email')
   city = user_details.get('City')
   name = user_details.get('fullName')
   return render_template('index.html',username=user_name,email_id=email_id,name=name)

@app.route('/register', methods=['POST','GET'])
def register():
   if request.method == 'POST':
      user_name = request.form.get("username")
      email_id = request.form.get("inputEmail")
      password = request.form.get("inputPassword")
      retyped_password = request.form.get("retypedPassword")
      city = request.form.get("inputCity")
      dob = request.form.get("inputDOB")
      fname = request.form.get("fname")
      mname = request.form.get("mname")
      lname = request.form.get("lname")
      checkbox = request.form.get("checkbox")

      #generate a password hash to securely store the password in database
      p_hash = generate_password_hash(password)
      #get username and email from existing database
      #and check if it already exists
      #if yes give error message
      #else proceed
      existing_username = user_data.find_one({'userName':user_name})
      if existing_username is None:
         existing_usermail = user_data.find_one({'Email':email_id})
         if existing_usermail is None:
            if password == retyped_password:
               user_data.insert(
                  {
                     'userName':user_name,
                     'Email':email_id,
                     'Password':p_hash,
                     'City':city,
                     'birthDate':dob,
                     'fullName': fname + mname + lname
                  }
               )
            else:
               return render_template('auth/register.html',message="Password not matched!")
            if checkbox == "on":
               #if sign in is checked
               #then redirect to the index page
               return render_template('index.html',username=user_name)
            else:
               #if the sign in not checked 
               #then redirect to the login page and show success message
               return render_template('auth/login.html',message="Registered successfully! Please login")
         else:
            return render_template('auth/register.html',message="Email alredy exists!")
      else:
         return render_template('auth/register.html',message="Username alredy exists!")
      #return user_name+"<br>"+email_id+"<br>"+password+"<br>"+retypedPassword+"<br>"+city+"<br>"+dob
   return render_template('auth/register.html')


@app.route('/profile')
def profile():
   if 'username' in session:
      user_details = user_data.find_one({'userName':session['username']})
      username = user_details.get('userName')
      name = user_details.get('fullName')
      email = user_details.get('Email')
      city = user_details.get('City')
      dob = user_details.get('dob')
   return render_template('profile.html',username=username,name=name,email=email,city=city,dob=dob)

@app.route('/updateProfile')
def updateProfile():
   return render_template('profile.html')

@app.route('/logout')
def logout():
   session.pop('username',None)
   session.clear()
   return render_template('home.html')

def changeColor():
   print("function called")


if __name__ == '__main__':
   app.run()
