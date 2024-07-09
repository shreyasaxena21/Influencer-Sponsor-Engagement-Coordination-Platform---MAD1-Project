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
        user = User.query.filter_by(user_name=uname, pwd=pwd).first() #Get existing user matched
        sponser_user = Sponser.query.filter_by(user_name=uname, pwd=pwd).first()
        if user and user.type == "admin" :
           campaign_summary = fetch_campaigns() #Calling
           return render_template("admin_dashboard_info.html", campaigns = campaign_summary )
        
        elif user and user.type == "general" :
            return render_template("influencer_dashboard_profile.html", username = user.full_name)
        
        elif sponser_user:
           return render_template("sponser_dashboard_profile.html") 
        
        return render_template("login.html",  msg="Invaid Credentials!!")
   
    else:
       return render_template("login.html",msg="")
    

@app.route("/influencer_signup", methods=["GET","POST"]) 
def influencer_signup():
    if request.method=="POST":
        email=request.form.get("email")
        full_name=request.form.get("fullname")
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        category=request.form.get("category")
        niche=request.form.get("niche")
        user = User.query.filter_by(user_name=uname).first() #Get existing user matched
        if not user:
            new_user=User(email=email,user_name=uname, pwd=pwd, full_name=full_name,  niche=niche, category=category)
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
        company_name=request.form.get("company_name")
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        indus=request.form.get("indus")
        user = Sponser.query.filter_by(user_name=uname).first() #Get existing user matched
        if not user:
            new_user=Sponser(email=email,user_name=uname, pwd=pwd, industry =indus, company_name=company_name)
            db.session.add(new_user)
            db.session.commit()
            return render_template("login.html", msg="")
        else:
            return render_template("sponser.html", msg="User already exists!")
    else:
       return render_template("sponser.html", msg="")

#User defined function
def fetch_campaigns():
    campaigns=Campaigns.query.filter_by(visibility = "public" ).all()
    campaign_list = {}
    for campaign in campaigns:
        if campaign.id not in campaign_list.keys():
            campaign_list[campaign.id] = [campaign.name, campaign.start_date]
    return campaign_list







