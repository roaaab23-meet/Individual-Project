from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

firebaseConfig = {
  "apiKey": "AIzaSyB2C3gVLgtL8kFkxJrRwP62MY2v6gWD89E",
  "authDomain": "project-5e7ce.firebaseapp.com",
  "projectId": "https://project-5e7ce-default-rtdb.asia-southeast1.firebasedatabase.app",
  "storageBucket": "project-5e7ce",
  "messagingSenderId": "project-5e7ce.appspot.com",
  "appId": "1001060069896",
  "measurementId": "1:1001060069896:web:25742221ba5530c7ce97bd" ,
  "databaseURL" : "https://project-5e7ce-default-rtdb.asia-southeast1.firebasedatabase.app/"
}

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()
db= firebase.database()
#Code goes below here

@app.route('/home', methods=['GET','POST'])
def home():
    posta=db.child("post").get().val()
    return render_template("index.html", posta=posta)

@app.route('/signup', methods=['GET','POST'])
def signup():
    error=""
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        try:
            login_session['user']=auth.create_user_with_email_and_password(email,password)
            user={"email":request.form['email'], "password":request.form['password'], "full name":request.form['full_name'],"username":request.form['username'], "bio":request.form['bio']}
            db.child("user").child(login_session['user']['localId']).set(user) 
            return redirect(url_for('home'))

        except:
            error="authentication failed"
    return render_template("signup.html")

@app.route('/post', methods=['GET','POST'])
def post():
    error=""
    if request.method=='POST':
        try:
            post={"title":request.form['title'],"write":request.form['write'],"pictures":request.form['pictures'], "uid":login_session['user']['localId'] }
            db.child("post").push(post)
        except:
            error="authentication failed"
    return render_template("post.html")


@app.route('/', methods=['GET', 'POST'])
def signin():
    error=""
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        try:
            login_session['user']=auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('home'))

        except:
            error="authentication failed"
    return render_template("signin.html")

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))


#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)