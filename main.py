from flask import Flask,request,render_template,redirect,session
import backend

app = Flask(__name__)


@app.route('/')
def home():
    return 'You are not logged in.'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with backend.connect("sql.db") as conn:
            backend.new_user_login(username,password,conn)
            session['username'] = username 
            return "login success!"
    return render_template("signup.html")

app.run()