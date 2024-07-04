from flask import Flask, render_template, request
from flask import current_app as app #Alias for current running app
from .models import *

@app.route("/")#refers base url 127.0.0.1.5000 local host
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET","POST"]) #it refers base url and login
def user_login():
    if request.method=="POST":
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        admin_user = Admin_Info.query.filter_by(user_name=uname, pwd=pwd).first() #Get existing user matched
        #sponser_user=Sponser_Info.query.filter_by(user_name=uname, pwd=pwd)
        #influencer_user=Influencer_Info.query.filter_by(user_name=uname, pwd=pwd)
        if admin_user and admin_user.is_admin:
            return render_template("admin_dashboard_info.html")
        
        #elif sponser_user and sponser_user.is_sponser:
         #  return render_template("sponser_dashboard_profile.html", username=  sponser_user.user_name)
        
        #elif influencer_user and influencer_user.is_influencer:
         #  return render_template("influencer_dashboard_profile.html", username=  influencer_user.user_name)
            
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
        category=request.form.get("category")
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
        company_name=request.form.get("company_name")
    return render_template("sponser.html")









