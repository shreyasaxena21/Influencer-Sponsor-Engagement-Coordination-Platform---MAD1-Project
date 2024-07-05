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
        admin_user = Admin.query.filter_by(user_name=uname, pass_hash=pwd).first() #Get existing user matched
        sponser_user=Sponser.query.filter_by(user_name=uname, pass_hash=pwd)
        influencer_user=Influencer.query.filter_by(user_name=uname, pass_hash=pwd)
        if admin_user and admin_user.is_admin:
            return render_template("admin_dashboard_info.html")
        
        elif sponser_user and sponser_user.is_sponser:
           return render_template("sponser_dashboard_profile.html", username = sponser_user.user_name)
        
        elif influencer_user and influencer_user.is_influencer:
           return render_template("influencer_dashboard_profile.html", username = influencer_user.user_name)
            
        else:
            return render_template("login.html",  msg="Invaid Credentials!!")
    else:
       return render_template("login.html",msg="")
    

@app.route("/influencer_signup", methods=["GET","POST"]) 
def influencer_signup():
    if request.method=="POST":
        email=request.form.get("email")
        full_name=request.form.get("full_name")
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        category=request.form.get("category")
        niche=request.form.get("niche")
        user = Influencer.query.filter_by(user_name=uname).first() #Get existing user matched
        if not user:
            new_user=Influencer(email=email,user_name=uname, pass_hash=pwd, name=full_name,  niche=niche, category=category)
            db.session.add(new_user)
            db.session.commit()
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









