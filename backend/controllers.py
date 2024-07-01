from flask import Flask, render_template, request
from flask import current_app as app #Alias for current running app
from .models import *

@app.route("/")#refers base url 127.0.0.1.5000 local host
def home():
    return "<h2> Welcome to Influencer - Sponser Coordination Platform </h2>"

@app.route("/login", methods=["GET","POST"]) #it refers base url and login
def user_login():
    if request.method=="POST":
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        user = User_Info.query.filter_by(user_name=uname, pwd=pwd).first() #Get existing user matched
        if user and user.role==0:
            return render_template("admin_dashboard_info.html")
        elif user and user.role==1:
            return render_template("influencer_dashboard_profile.html", username=user.user_name)
        else:
            return render_template("login.html",  msg="Invaid Credentials!!")
    else:
       return render_template("login.html",msg="")


@app.route("/influencer_signup", methods=["GET","POST"]) 
def influencer_signup():
    if request.method=="POST":
        email=request.form.get("email")
        fname=request.form.get("fname")
        lname=request.form.get("lname")
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        user = User_Info.query.filter_by(user_name=uname).first() #Get existing user matched
        if not user:
            new_user=User_Info(email=email, fname=fname, lname=lname,user_name=uname, pwd=pwd)
            db.session.add(new_user)
            db.commit()
            return render_template("login.html", msg="")
        else:

            return render_template("influencer.html", msg="User already exists!")
    else:
       return render_template("influencer.html",msg="")


@app.route("/sponser_signup", methods=["GET","POST"]) 
def sponser_signup():
    if request.method=="POST":
        email=request.form.get("email")
        fname=request.form.get("fname")
        lname=request.form.get("lname")
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        indus=request.form.get("indus")
    return render_template("sponser.html")


