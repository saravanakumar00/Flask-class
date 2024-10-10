"""
Fix : code bug

Add 


"""

from flask import Flask,render_template,request,redirect,session,url_for
from flask_mail import Mail,Message

import random
import sqlite3
from urllib.parse import urlencode
app=Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USERNAME']='saravanakumar364521@gmail.com'
app.config['MAIL_PASSWORD']=""
app.config['MAIL_TLS']=True
mail=Mail(app)

app.secret_key='fksdk'

conn=sqlite3.Connection('user.db',check_same_thread=False)
conn.execute('CREATE TABLE IF NOT EXISTS santhosh(id integer primary key autoincrement,username text,password text)')

# Otp generating
def  generator():
    otp=random.randint(1000,9999)
    return str(otp)
@app.route('/sentotp',methods=['GET','POST'])
def sent_otp():
    if "username" in session:
        username=session['username']
        otp=generator()
        msg=Message("OTP Verification",sender="saravanakumar364521@gmail.com",recipients=[username])
        msg.body=f"Your otp is {otp}"
        mail.send(msg)
        return render_template("project5.html")
    else:
        return "Username not add in Session"
    


@app.route("/checkotp",methods=['POST'])
def checkotp():
    if "otp"in request.form:   # check if otp is in the form data
        otp=request.form['otp'] # Retrieve the otp form the form data
        if "otp" in session and session['otp']==otp:
            message="OTP Verified successfully"
            query_string=urlencode({"message":message})
            return redirect(url_for("home")+"?"+query_string)
        else:
            return 'OTP does not match'
    else:
        return "No OTP provided"
    




@app.route('/')
def home():
    return render_template("project1.html")


@app.route("/signin",methods=['GET','POST'])
def signin():
    if request.method=='POST':
        username=request.form['name']
        password=request.form['pass']
        conn.execute("insert into santhosh(username,password)values(?,?)",(username,password))
        conn.commit()
        session['username']=username
        return redirect('/sendotp')
    return render_template('project2.html')


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        # check username and password match
        cursor=conn.execute("SELECT * from santhosh where username=? AND password=?",username,password)
        user=cursor.fetchone()
        if user:
            session['username']=username
            return 'Login successfull'
        else:
            return "Invalid username or password"
    return render_template('project3.html')

@app.route('/display')
def print_user():
    cursor=conn.execute("select*from santhosh")
    users=cursor.fetchall()
    return render_template('project4.html',users=users)



@app.route('/delete/<int:id>')
def deleteuser(id):
    #conn.execute("delete from santhosh where id=?",(id))
    #conn.commit()
    """Another way if Delete"""
    connection=sqlite3.connect('user.db')
    cursor=connection.cursor()
    cursor.execute('delete from santhosh where id=?',(id))
    connection.commit()
    connection.close()
    return redirect("/display")

if __name__=="__main__":
    app.run(debug=True)


