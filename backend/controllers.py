from flask import Flask, render_template, request, flash, url_for, redirect
from flask import current_app as app #Alias for current running app
from .models import *
import datetime


@app.route("/")#refers base url 127.0.0.1.5000 local host
def home():
    return render_template("home.html")



#-------------------------------------------------------Influencer Signup-------------------------------------------------------

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
            new_user=User(email=email,user_name=uname, search_name = raw(full_name), pwd=pwd, full_name=full_name,  niche=niche, followers = followers, category=category)
            db.session.add(new_user)
            db.session.commit()
            return render_template("login.html", msg="")
        else:
           return render_template("influencer.html", msg="User already exists!")
    else:
       return render_template("influencer.html",msg="")

#-------------------------------------------------------Sponser signup-------------------------------------------------------

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
            new_user=Sponser(email=email,user_name=uname, search_name = uname , pwd=pwd, industry =indus, company_name=company_name)
            db.session.add(new_user)
            db.session.commit()
            return render_template("login.html", msg="")
        else:
            return render_template("sponser.html", msg="User already exists!")
    else:
       return render_template("sponser.html", msg="")
    
#-------------------------------------------------------Login-------------------------------------------------------

@app.route("/login", methods=["GET","POST"]) #it refers base url and login
def user_login():
    if request.method=="POST":
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        user = User.query.filter_by(user_name=uname, pwd=pwd).first() #Get existing user matched
        sponser_user = Sponser.query.filter_by(user_name=uname, pwd=pwd).first()
        if user and user.type == "admin" :
           return redirect('/admin/dashboard')
        
        elif user and user.type == "general" :
            return redirect(f'/influencer/dashboard/{user.id}')
        
        elif sponser_user:
           return redirect(f'/sponser/dashboard/{sponser_user.id}')
           
        
        return render_template("login.html",  msg="Invalid Credentials!!")
   
    else:
       
       return render_template("login.html",msg="")
    

#-------------------------------------------------------Dashboard routes------------------------------------------------------------

@app.route('/admin/dashboard')
def admin_dashboard():
    admin = User.query.filter_by(type = "admin")
    campaign_summary = fetch_campaigns() #Calling
    ad_request_summary = fetch_ad_requests()
    return render_template("admin_dashboard_info.html", campaigns = campaign_summary , ad_requests = ad_request_summary)
    
@app.route('/influencer/dashboard/<int:i_id>', methods=['GET', 'POST'])
def influencer_dashboard(i_id):
    influencer = User.query.get(i_id)
    campaign_summary = fetch_campaigns()
    requests = influencer.ad_request
    return render_template("influencer_dashboard_profile.html",  influencer = influencer, campaigns = campaign_summary, ad_requests = requests)

@app.route('/sponser/dashboard/<int:s_id>',  methods=['GET', 'POST'])
def sponser_dashboard(s_id):
    sponser = Sponser.query.get(s_id)
    campaign_summary = sponser.campaigns
    return render_template("sponser_dashboard_profile.html", sponser = sponser, campaigns=campaign_summary) 

#-------------------------------------------------------User defined function-------------------------------------------------------

def fetch_campaigns():
    campaigns=Campaigns.query.filter_by(visibility = "Public" ).all()
    campaign_list = {}
    for campaign in campaigns: 
        if campaign.id not in campaign_list.keys():
            campaign_list[campaign.id] = [campaign.name, campaign.start_date, campaign.end_date, campaign.budget, campaign.niche]
    return campaign_list

def fetch_ad_requests():
    ad_request = Ad_request.query.filter_by(visibility = "Public" ).all()
    ad_request_list = {}
    for ad in ad_request: 
        if ad.id not in ad_request_list.keys():
            ad_request_list[ad.id] = [ad.name, ad.status]
    return ad_request_list

def fetch_influencers():
    influencer = User.query.filter_by(type = 'general' ).all()
    influencer_list = {}
    for user in influencer: 
        if user.id not in influencer_list.keys():
            influencer_list[user.id] = [user.full_name, user.category, user.niche, user.followers]
    return influencer_list

def fetch_sponsers():
    sponsers = Sponser.query.filter().all()
    sponser_list = {}
    for sponser in sponsers: 
        if sponser.id not in sponser_list.keys():
            sponser_list[sponser.id] = [sponser.company_name, sponser.industry]
    return sponser_list




def fetch_campaign_info():
    campaign_info = Campaigns.query.filter().all()
    return campaign_info

def fetch_sponser_info(id):
    sponser_info = Sponser.query.filter_by(id=id).first()
    return sponser_info

def fetch_influencer_info(id):
    influencer_info = User.query.filter_by(id=id).first()
    return influencer_info

# def fetch_campaign_id(id):
#     camp_id = Campaigns.query.filter_by(sponser_id = id)
#     return camp_id

def get_campaign_by_id(campaign_id):
    return Campaigns.query.get(campaign_id)

def raw(text): #to convert the searched word to raw string
    split_list = text.split() #converts to a list
    search_word = ''
    for word in split_list:
        search_word += word.lower()
    return search_word


#-------------------------------------------------------Campaign routes-------------------------------------------------------

@app.route("/sponser/dashboard/campaign/<int:s_id>", methods = ["GET", "POST"])
def sponser_dashboard_campaign(s_id):
    if request.method == "GET":
        sponser = Sponser.query.get(s_id)
        # campaign_info = fetch_campaign_info()
        
        return render_template("sponser_dashboard_campaigns.html", sponser = sponser, campaigns = sponser.campaigns)

@app.route("/add/campaign/<int:s_id>", methods = ["GET", "POST"])
def add_campaign(s_id):
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        #start_date_str = request.form.get("start_date")
        start_date = str(datetime.date.today().strftime("%d/%m/%Y"))
        end_date = request.form.get("end_date")
        #end_date = datetime.strptime(end_date_str, '%d/%m/%Y').date()
        budget = request.form.get("budget")
        visibility = request.form.get("visibility")
        goals = request.form.get("goals")
        niche = request.form.get("niche")
        sponser_id = request.form.get("sponser_id")
        campaign_obj = Campaigns(name = title, search_name = raw(title) , description=description, budget = budget,start_date = start_date, end_date = end_date, visibility = visibility, goals = goals, niche=niche, sponser_id = sponser_id)
        db.session.add(campaign_obj)
        db.session.commit()
        sponser = Sponser.query.get(s_id)
        #campaign_info = fetch_campaign_info() 
        return render_template("sponser_dashboard_campaigns.html",  sponser=sponser, campaigns = sponser.campaigns)
    return render_template("sponser_dashboard_profile.html")


@app.route("/edit/campaign/<int:s_id>", methods = ["GET", "POST"])
def edit_campaign(s_id):
    if request.method=="POST":
        new_title=request.form.get("title")
        new_description=request.form.get("description")
        new_goals=request.form.get("goals")
        new_budget=request.form.get("budget")
        new_visibility=request.form.get("visibility")
        new_niche=request.form.get("niche")
        campaign_obj=Campaigns.query.filter_by(sponser_id = s_id ,name = new_title).first()
        campaign_obj.name = new_title
        campaign_obj.description = new_description
        campaign_obj.goals = new_goals
        campaign_obj.budget = new_budget
        campaign_obj.visibility = new_visibility
        campaign_obj.niche = new_niche
        db.session.commit()
        sponser = Sponser.query.get(s_id)
        return render_template("sponser_dashboard_campaigns.html", sponser = sponser, campaigns = sponser.campaigns)
   

@app.route("/delete/campaign/<int:s_id>",methods=["GET","POST"])
def delete_campaign(s_id):
    if request.method=="POST":
        title=request.form.get("title")
        campaign_obj=Campaigns.query.filter_by(sponser_id = s_id , name = title).first()
        db.session.delete(campaign_obj)
        db.session.commit()
        sponser = Sponser.query.get(s_id)
        return render_template("sponser_dashboard_campaigns.html",sponser = sponser, campaigns = sponser.campaigns)



@app.route("/sponser/dashboard/view/campaign/<campaign_id>", methods = ["GET", "POST"])
def sponser_dashboard_view_campaign(campaign_id):
    if request.method == "GET":
        # campaign_name = fetch_campaign_name(campaign_id)
        campaigns = fetch_campaign_info()
        campaign = get_campaign_by_id(campaign_id)
        return render_template("sponser_dashboard_view_campaign.html", campaign = campaign, campaigns = campaigns )


 
#-------------------------------------------------------Ad Request Routes-------------------------------------------------------

@app.route("/sponser/dashboard/ad_request", methods = ["GET"])
def sponser_dashboard_ad_request():
    if request.method == "GET":
        #campaign_info = get_campaign_by_id()
        campaign_info = fetch_campaign_info()
        
        return render_template("sponser_dashboard_campaigns.html", campaigns = campaign_info)
    
@app.route("/add/ad_request/<int:campaign_id>", methods = ["GET", "POST"])
def add_adrequest(campaign_id):
    if request.method == "POST":
        ad_name = request.form.get("ad_name")
        description = request.form.get("description")
        payment = request.form.get("payment")
        terms = request.form.get("terms")
        influencer = request.form.get("influencer")
        campaign_id = request.form.get("campaign_id")
        status = request.form.get("status")
        ad_obj = Ad_request(name = ad_name, message = description, payment_amount = payment , requirements = terms, influencer_id = influencer, campaign_id = campaign_id, status = status)
        db.session.add(ad_obj)
        db.session.commit()
        #sponser_info = fetch_sponser_info(sponser_id)
        campaign = Campaigns.query.get(campaign_id)
        return render_template("sponser_dashboard_view_campaign.html", campaign=campaign , campaigns = campaign.ad_requests)
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
        campaign_obj=Ad_request.query.filter_by(name = ad_name).first()
        db.session.delete(campaign_obj)
        db.session.commit()
        campaign = fetch_campaign_info() 
        return render_template("sponser_dashboard_view_campaign.html", campaigns = campaign.ad_requests)


#-------------------------------------------------------Sponser Routes-------------------------------------------------------

@app.route("/sponser/dashboard/profile", methods = ["GET", "POST"])
def sponser_dashboard_profile():
    campaign_summary = fetch_campaigns()
    return render_template("sponser_dashboard_profile.html",campaigns=campaign_summary)



@app.route("/sponser/dashboard/find", methods = ["GET", "POST"])
def sponser_dashboard_find():
    influencers = fetch_influencers()
    return render_template("sponser_dashboard_find.html", influencers = influencers)

@app.route('/sponser/search', methods=["GET"])
def text_search_sponser():
    search_word = request.args.get('search_word')
    search_word = "%" + raw(search_word) + "%"
    search_niche = "%" + search_word.lower() + "%"
    search_followers = "%" + raw(search_word) + "%"
    i_names = User.query.filter(User.search_name.like(search_word)).all()
    i_niche = User.query.filter(User.niche.like(search_niche)).all()
    i_followers = User.query.filter(User.followers.like(search_followers)).all()
    search_results = i_names + i_niche + i_followers
    return render_template('sponser_search.html', search_results = search_results)

@app.route('/edit/profile/<int:s_id>')
def edit_profile(s_id):
    sponser = Sponser.query.get(s_id)
    return render_template("edit_sponser_profile.html", sponser = sponser)

@app.route('/edit/profile/sponser/<int:s_id>', methods=["GET", "POST"])
def edit_sponser_profile(s_id):
    if request.method=="POST":
        new_user_name = request.form.get("user_name")
        new_password = request.form.get("password")
        user_obj = Sponser.query.filter_by(id = s_id, user_name = new_user_name).first()
        user_obj.user_name = new_user_name
        user_obj.password = new_password
        db.ssession.commit()
        sponser = Sponser.query.get(s_id)
        return render_template("edit_sponser_profile.html", sponser = sponser)
    return render_template("influencer_dashboard_profile.html")

#-------------------------------------------------------Influencer routes-------------------------------------------------------

@app.route("/influencer/dashboard/find")
def influencer_dashboard_find():
    campaign_summary = fetch_campaigns()
    return render_template("influencer_dashboard_find.html", campaigns = campaign_summary)

@app.route("/influencer/dashboard/profile")
def influencer_dashboard_profile():
    campaign_summary = fetch_campaigns()
    ad_request_summary = fetch_ad_requests()
    return render_template("influencer_dashboard_profile.html", campaigns=campaign_summary, ad_requests=ad_request_summary)


@app.route('/influencer/search', methods=["GET"])
def text_search():
    search_word = request.args.get('search_word')
    search_word = "%" + raw(search_word) + "%"
    search_niche = "%" + search_word.lower() + "%"
    c_names = Campaigns.query.filter(Campaigns.search_name.like(search_word)).all()
    c_niche = Campaigns.query.filter(Campaigns.niche.like(search_niche)).all()
    search_results = c_names + c_niche
    return render_template('influencer_search.html', search_results = search_results)

@app.route('/edit/profile/page/<int:i_id>')
def edit_profile_page(i_id):
    user = User.query.get(i_id)
    return render_template("edit_influencer_profile.html", user = user)

@app.route('/edit/profile/influencer<int:i_id>', methods=["GET", "POST"])
def edit_influencer_profile(i_id):
    if request.method=="POST":
        new_user_name = request.form.get("user_name")
        new_password = request.form.get("password")
        user_obj = User.query.filter_by(id = i_id, user_name = new_user_name).first()
        user_obj.user_name = new_user_name
        user_obj.password = new_password
        db.session.commit()
        user = User.query.get(i_id)
        return render_template("edit_influencer_profile.html", user_name = user.user_name, username = user.full_name)
    return render_template("influencer_dashboard_profile.html")

#-------------------------------------------------------Admin routes-------------------------------------------------------

@app.route("/admin/dashboard/info")
def admin_dashboard_info():
    campaign_summary = fetch_campaigns() 
    ad_request_summary = fetch_ad_requests()
    return render_template("admin_dashboard_info.html", campaigns = campaign_summary , ad_requests = ad_request_summary)

@app.route("/admin/dashboard/find")
def admin_dashboard_find():
    influencers = fetch_influencers()
    sponsers = fetch_sponsers()
    return render_template("admin_dashboard_find.html", influencers=influencers, sponsers= sponsers)

@app.route('/admin/search', methods=["GET"])
def admin_influencer_text_search():
    search_word = request.args.get('search_word')
    search_word = "%" + raw(search_word) + "%"
    if search_word == User.query.filter_by(search_name = search_word):
        i_names = User.query.filter(User.search_name.like(search_word)).all()
        search_results = i_names 
        return render_template('admin_influencer_search.html', search_results = search_results)
    else:
        s_names = Sponser.query.filter(Sponser.search_name.like(search_word)).all()
        search_results = s_names 
        return render_template('admin_sponser_search.html', search_results = search_results)


#-------------------------------------------------------View Button Routes-------------------------------------------------------

@app.route('/view/campaign/<int:campaign_id>')
def view(campaign_id):
    campaign = Campaigns.query.get(campaign_id)
    return render_template("admin_view.html", campaign=campaign)

@app.route('/view/campaign/influencer/<int:campaign_id>')
def view_influencer(campaign_id):
    campaign = Campaigns.query.get(campaign_id)
    return render_template("influencer_view.html", campaign=campaign)

@app.route('/view/campaign/sponser/<int:campaign_id>')
def view_sponser(campaign_id):
    campaign = Campaigns.query.get(campaign_id)
    return render_template("sponser_view.html", campaign=campaign)

@app.route('/admin/view/user/<int:i_id>')
def admin_view_user(i_id):
    user = User.query.get(i_id)
    return render_template("admin_users_view.html", user=user)

@app.route('/admin/view/sponser/<int:s_id>')
def admin_view_sponser(s_id):
    sponser = Sponser.query.get(s_id)
    return render_template("admin_sponser_view.html", sponser = sponser)
    
    




















