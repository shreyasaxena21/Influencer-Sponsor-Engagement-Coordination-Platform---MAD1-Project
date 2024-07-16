from flask import Flask, render_template, request, flash, url_for
from flask import current_app as app #Alias for current running app
from .models import *


@app.route("/")#refers base url 127.0.0.1.5000 local host
def home():
    return render_template("home.html")



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
            campaign_summary = fetch_campaigns()
            return render_template("influencer_dashboard_profile.html", username = user.full_name, campaigns = campaign_summary)
        
        elif sponser_user:
           campaign_summary = fetch_campaigns()
           return render_template("sponser_dashboard_profile.html", id = sponser_user.id, username = sponser_user.user_name, campaigns=campaign_summary) 
        
        return render_template("login.html",  msg="Invalid Credentials!!")
   
    else:
       return render_template("login.html",msg="")
    
    
#User defined function
def fetch_campaigns():
    campaigns=Campaigns.query.filter_by(visibility = "Public" ).all()
    campaign_list = {}
    for campaign in campaigns:
        if campaign.id not in campaign_list.keys():
            campaign_list[campaign.id] = [campaign.name, campaign.start_date]
    return campaign_list

def fetch_campaign_info():
    campaign_info = Campaigns.query.filter().all()
    return campaign_info


@app.route("/sponser/dashboard/campaign", methods = ["GET", "POST"])
def sponser_dashboard_campaign():
    if request.method == "GET":
        campaign_info = fetch_campaign_info()

        return render_template("sponser_dashboard_campaigns.html", campaigns = campaign_info)

@app.route("/add_campaign", methods = ["GET", "POST"])
def add_campaign():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        start_date_str = request.form.get("start_date")
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date_str = request.form.get("end_date")
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        budget = request.form.get("budget")
        visibility = request.form.get("visibility")
        goals = request.form.get("goals")
        niche = request.form.get("niche")
        sponser_id = request.form.get("sponser_id")
        campaign_obj = Campaigns(name = title, description=description, budget = budget,start_date = start_date, end_date = end_date, visibility = visibility, goals = goals, niche=niche, sponser_id = sponser_id)
        db.session.add(campaign_obj)
        db.session.commit()
        campaign_info = fetch_campaign_info() 
        return render_template("sponser_dashboard_campaigns.html", campaigns = campaign_info)
    return render_template("sponser_dashboard_profile.html")


def fetch_campaign_name(campaign_name):
    name = Campaigns.query.filter_by(name = campaign_name).first()
    return name


@app.route("/sponser/dashboard/view/campaign/<campaign_name>", methods = ["GET", "POST"])
def sponser_dashboard_view_campaign(campaign_name):
    if request.method == "GET":
        campaign_name = fetch_campaign_name(campaign_name)
        campaign_info = fetch_campaign_info()
        return render_template("sponser_dashboard_view_campaign.html", campaigns = campaign_info, name = campaign_name)


 
        

#Sponser Routes
@app.route("/sponser/dashboard/profile", methods = ["GET", "POST"])
def sponser_dashboard_profile():
    return render_template("sponser_dashboard_profile.html")



@app.route("/sponser/dashboard/find", methods = ["GET", "POST"])
def sponser_dashboard_find():
    return render_template("sponser_dashboard_find.html")




















