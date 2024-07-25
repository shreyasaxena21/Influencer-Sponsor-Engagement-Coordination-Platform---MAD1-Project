from flask import Flask, render_template, request, flash, url_for
from flask import current_app as app #Alias for current running app
from .models import *
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager, login_user, login_required, logout_user,current_user
from flask_bcrypt import Bcrypt
import datetime


@app.route("/")#refers base url 127.0.0.1.5000 local host
def home():
    return render_template("home.html")



#Influencer Signup
@app.route("/influencer_signup", methods=["GET","POST"]) 
def influencer_signup():
    if request.method=="POST":
        email=request.form.get("email")
        full_name=request.form.get("fullname")
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        category=request.form.get("category")
        niche=request.form.get("niche")
        followers = request.form.get("followers") 
        user = User.query.filter_by(user_name=uname).first() #Get existing user matched
        if not user:
            new_user=User(email=email,user_name=uname, pwd=pwd, full_name=full_name,  niche=niche, followers = followers, category=category)
            db.session.add(new_user)
            db.session.commit()
            return render_template("login.html", msg="")
        else:
           return render_template("influencer.html", msg="User already exists!")
    else:
       return render_template("influencer.html",msg="")

#Sponser signup
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
    
#login
@app.route("/login", methods=["GET","POST"]) #it refers base url and login
def user_login():
    if request.method=="POST":
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        user = User.query.filter_by(user_name=uname, pwd=pwd).first() #Get existing user matched
        sponser_user = Sponser.query.filter_by(user_name=uname, pwd=pwd).first()
        if user and user.type == "admin" :
           campaign_summary = fetch_campaigns() #Calling
           ad_request_summary = fetch_ad_requests()
           return render_template("admin_dashboard_info.html", campaigns = campaign_summary , ad_requests = ad_request_summary)
        
        elif user and user.type == "general" :
            campaign_summary = fetch_campaigns()
            ad_request_summary = fetch_ad_requests()
            return render_template("influencer_dashboard_profile.html", user_id = user.id, username = user.full_name, campaigns = campaign_summary, ad_requests = ad_request_summary)
        
        elif sponser_user:
           campaign_summary = fetch_campaigns()
           return render_template("sponser_dashboard_profile.html", username = sponser_user.user_name, campaigns=campaign_summary) 
        
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

def fetch_ad_requests():
    ad_request = Ad_request.query.filter_by(visibility = "Public" ).all()
    ad_request_list = {}
    for ad in ad_request: 
        if ad.id not in ad_request_list.keys():
            ad_request_list[ad.id] = [ad.name, ad.status]
    return ad_request_list




def fetch_campaign_info():
    campaign_info = Campaigns.query.filter().all()
    return campaign_info

def fetch_sponser_info(id):
    sponser_info = Sponser.query.filter_by(id=id).first()
    return sponser_info

# def fetch_campaign_id(id):
#     camp_id = Campaigns.query.filter_by(sponser_id = id)
#     return camp_id

def get_campaign_by_id(campaign_id):
    return Campaigns.query.get(campaign_id)


#campaign routes
@app.route("/sponser/dashboard/campaign/<int:sponser_id>", methods = ["GET", "POST"])
def sponser_dashboard_campaign(sponser_id):
    if request.method == "GET":
        sponser_info = fetch_sponser_info(sponser_id)
        campaign_info = fetch_campaign_info()
        
        return render_template("sponser_dashboard_campaigns.html", id = sponser_info.id, campaigns = sponser_info.campaigns)

@app.route("/add/campaign/<int:sponser_id>", methods = ["GET", "POST"])
def add_campaign(sponser_id):
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        #start_date_str = request.form.get("start_date")
        start_date = str(datetime.date.today().strftime("%d/%m%Y"))
        end_date = request.form.get("end_date")
        #end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        budget = request.form.get("budget")
        visibility = request.form.get("visibility")
        goals = request.form.get("goals")
        niche = request.form.get("niche")
        sponser_id = request.form.get("sponser_id")
        campaign_obj = Campaigns(name = title, description=description, budget = budget,start_date = start_date, end_date = end_date, visibility = visibility, goals = goals, niche=niche, sponser_id = sponser_id)
        db.session.add(campaign_obj)
        db.session.commit()
        sponser_info = fetch_sponser_info(sponser_id)
        campaign_info = fetch_campaign_info() 
        return render_template("sponser_dashboard_campaigns.html",  id = sponser_info.id, campaigns = campaign_info)
    return render_template("sponser_dashboard_profile.html")


@app.route("/edit/campaign/<int:sponser_id>", methods = ["GET", "POST"])
def edit_campaign(sponser_id):
    if request.method=="POST":
        new_title=request.form.get("title")
        new_description=request.form.get("description")
        campaign_obj=Campaigns.query.filter_by(sponser_id = sponser_id ,name = new_title).first()
        campaign_obj.name = new_title
        campaign_obj.description = new_description
        db.session.commit()
        sponser_info = fetch_sponser_info(sponser_id)
        return render_template("sponser_dashboard_campaigns.html",id=sponser_info.id, campaigns = sponser_info.campaigns)
   

@app.route("/delete/campaign/<int:sponser_id>",methods=["GET","POST"])
def delete_campaign(sponser_id):
    if request.method=="POST":
        title=request.form.get("title")
        campaign_obj=Campaigns.query.filter_by(sponser_id = sponser_id , name = title).first()
        db.session.delete(campaign_obj)
        db.session.commit()
        sponser_info = fetch_sponser_info(sponser_id)
        return render_template("sponser_dashboard_campaigns.html",id=sponser_info.id, campaigns = sponser_info.campaigns)



@app.route("/sponser/dashboard/view/campaign/<campaign_id>", methods = ["GET", "POST"])
def sponser_dashboard_view_campaign(campaign_id):
    if request.method == "GET":
        # campaign_name = fetch_campaign_name(campaign_id)
        campaigns = fetch_campaign_info()
        campaign = get_campaign_by_id(campaign_id)
        return render_template("sponser_dashboard_view_campaign.html", campaign = campaign, campaigns = campaigns )


 
#Ad Request Routes
@app.route("/sponser/dashboard/ad_request", methods = ["GET", "POST"])
def sponser_dashboard_ad_request():
    if request.method == "GET":
        #campaign_info = get_campaign_by_id()
        campaign_info = fetch_campaign_info()
        
        return render_template("sponser_dashboard_campaigns.html", campaigns = campaign_info)
    
@app.route("/add/ad_request", methods = ["GET", "POST"])
def add_adrequest():
    if request.method == "POST":
        ad_name = request.form.get("ad_name")
        description = request.form.get("description")
        payment = request.form.get("payment")
        terms = request.form.get("terms")
        influencer = request.form.get("influencer")
        campaign_id = request.form.get("campaign_id")
        ad_obj = Ad_request(name = ad_name, message = description, payment_amount = payment , requirements = terms, influencer_id = influencer, campaign_id = campaign_id)
        db.session.add(ad_obj)
        db.session.commit()
        #sponser_info = fetch_sponser_info(sponser_id)
        campaign = fetch_campaign_info() 
        return render_template("sponser_dashboard_view_campaign.html", campaigns = campaign.ad_requests)
    return render_template("sponser_dashboard_profile.html")


@app.route("/edit/ad_request", methods = ["GET", "POST"])
def edit_ad_request():
    if request.method=="POST":
        ad_id = request.form.get("ad_id")
        new_ad_name=request.form.get("ad_name")
        new_terms = request.form.get("terms")
        new_status = request.form.get("status")
        new_payment = request.form.get("payment")
        new_influencer = request.form.get("influencer")
        ad_obj = Ad_request.query.filter_by(id = ad_id, name = new_ad_name).first()
        ad_obj.name = new_ad_name
        ad_obj.requirements = new_terms
        ad_obj.status = new_status
        ad_obj.payment_amount = new_payment
        ad_obj.inlfluencer_id = new_influencer
        db.session.commit()
        campaign = fetch_campaign_info() 
        return render_template("sponser_dashboard_view_campaign.html", campaigns = campaign.ad_requests)
    
@app.route("/delete/ad_request",methods=["GET","POST"])
def delete_ad_request():
    if request.method=="POST":
        ad_name=request.form.get("ad_name")
        campaign_obj=Campaigns.query.filter_by(name = ad_name).first()
        db.session.delete(campaign_obj)
        db.session.commit()
        campaign = fetch_campaign_info() 
        return render_template("sponser_dashboard_view_campaign.html", campaigns = campaign.ad_requests)


#Sponser Routes
@app.route("/sponser/dashboard/profile", methods = ["GET", "POST"])
def sponser_dashboard_profile():
    return render_template("sponser_dashboard_profile.html")



@app.route("/sponser/dashboard/find", methods = ["GET", "POST"])
def sponser_dashboard_find():
    return render_template("sponser_dashboard_find.html")




#admin routes
@app.route("/admin/dashboard/info")
def admin_dashboard_info():
    return render_template("admin_dashboard_info.html")

@app.route("/admin/dashboard/find")
def admin_dashboard_find():
    return render_template("admin_dashboard_find.html")

#user defined function for searching
def search_database(query):
    results = []

    # Search campaigns
    campaigns = Campaigns.query.filter(Campaigns.name.ilike(f'%{query}%')).all()
    for campaign in campaigns:
        results.append(f"Campaign: {campaign.name}")

    # Search influencers
    influencers = User.query.filter(User.user_name.ilike(f'%{query}%')).all()
    for influencer in influencers:
        results.append(f"Influencer: {influencer.name}")

    # Search sponsors
    sponsors = Sponser.query.filter(Sponser.user_name.ilike(f'%{query}%')).all()
    for sponsor in sponsors:
        results.append(f"Sponsor: {sponsor.name}")

    return results


@app.route('/admin/search', methods=["POST"])
def admin_search():
    query = request.args.get('query')
    search_results = search_database(query)
    return render_template('admin_dashboard_find.html', search_results = search_results)



















