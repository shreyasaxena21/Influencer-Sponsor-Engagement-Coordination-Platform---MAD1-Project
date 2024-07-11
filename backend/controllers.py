from flask import Flask, render_template, request, flash
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
           sponser_info = fetch_sponser_info(sponser_user.id)
           return render_template("sponser_dashboard_profile.html", id = sponser_info.id ,username= sponser_user.user_name, campaigns = sponser_info.campaign) 
        
        return render_template("login.html",  msg="Invalid Credentials!!")
   
    else:
       return render_template("login.html",msg="")
    


#Influencer routes
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

#Sponser routes
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
    

@app.route("/add/campaigns/<int:sponser_id>", methods = ["GET", "POST"])
def new_campaigns(sponser_id):
    if request.method=="POST":
        title = request.form.get("title")
        description = request.form.get("description")
        niche = request.form.get("niche")
        date = request.form.get("date")
        campaign_obj = Campaigns(name = title, description=description, niche=niche, start_date = date, sponser_id = id)
        db.session.add(campaign_obj)
        db.session.commit()
        sponser_info = fetch_sponser_info(sponser_id)
        return render_template("sponser_dashboard_profile.html", id = sponser_info.id ,username= sponser_info.user_name, campaigns = sponser_info.campaign) 
        

@app.route("/sponser/dashboard/profile", methods = ["GET", "POST"])
def sponser_dashboard_profile():
    return render_template("sponser_dashboard_profile.html")

@app.route("/sponser/dashboard/campaign", methods = ["GET", "POST"])
def sponser_dashboard_campaign():
    return render_template("sponser_dashboard_campaigns.html")

@app.route("/sponser/dashboard/find", methods = ["GET", "POST"])
def sponser_dashboard_find():
    return render_template("sponser_dashboard_find.html")








#User defined function
def fetch_campaigns():
    campaigns=Campaigns.query.filter_by(visibility = "public" ).all()
    campaign_list = {}
    for campaign in campaigns:
        if campaign.id not in campaign_list.keys():
            campaign_list[campaign.id] = [campaign.name, campaign.start_date]
    return campaign_list

def fetch_sponser_info(id):
    sponser_info = Sponser.query.filter_by(id=id).first()
    return sponser_info







