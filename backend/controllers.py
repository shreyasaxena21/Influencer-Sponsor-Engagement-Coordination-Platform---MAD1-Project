from flask import Flask, render_template, request, flash, url_for, redirect
from flask import current_app as app #Alias for current running app
from .models import *
import datetime
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("Agg") #This make sure that the application run within the server



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
            if user.is_flagged == "False":
                return redirect(f'/influencer/dashboard/{user.id}')
            return render_template("login.html",msg="You are being Flagged by the admin. Contact Admin for further details!!") 
        
        elif sponser_user:
           if sponser_user.is_flagged == "False":
                return redirect(f'/sponser/dashboard/{sponser_user.id}')
           return render_template("login.html",msg="Your company has been Flagged by the admin. Contact Admin for further details!!") 
           
        
        return render_template("login.html",  msg="Invalid Credentials!!")
   
    else:
       
       return render_template("login.html",msg="")
    

#-------------------------------------------------------Dashboard routes------------------------------------------------------------

@app.route('/admin/dashboard')
def admin_dashboard():
    admin = User.query.filter_by(type = "admin")
    campaign_summary = fetch_campaigns() #Calling
    flagged_user = fetch_flagged_user()
    flagged_sponser = fetch_flagged_sponser()
    return render_template("admin_dashboard_info.html", campaigns = campaign_summary, flagged_user=flagged_user, flagged_sponser=flagged_sponser )
    
@app.route('/influencer/dashboard/<int:i_id>', methods=['GET', 'POST'])
def influencer_dashboard(i_id):
    influencer = User.query.get(i_id)
    campaign_summary = fetch_campaigns()
    requests = Sponser_Request.query.filter_by(influencer_id = i_id)
    return render_template("influencer_dashboard_profile.html",  influencer = influencer, campaigns = campaign_summary, requests = requests)

@app.route('/sponser/dashboard/<int:s_id>',  methods=['GET', 'POST'])
def sponser_dashboard(s_id):
    sponser = Sponser.query.get(s_id)
    requests = Influencer_Request.query.filter_by(sponser_id = s_id).all()
    campaign_summary = sponser.campaigns
    return render_template("sponser_dashboard_profile.html", sponser = sponser, campaigns=campaign_summary, requests = requests) 

#-------------------------------------------------------User defined function-------------------------------------------------------

def fetch_campaigns():
    campaigns=Campaigns.query.filter_by(visibility = "Public" ).all()
    campaign_list = {}
    for campaign in campaigns: 
        if campaign.id not in campaign_list.keys():
            campaign_list[campaign.id] = [campaign.name, campaign.niche, campaign.end_date, campaign.budget, campaign.start_date, campaign.sponser_id]
    return campaign_list

def fetch_ad_requests():
    ad_request = Ad_request.query.filter_by(visibility = "Public" ).all()
    ad_request_list = {}
    for ad in ad_request: 
        if ad.id not in ad_request_list.keys():
            ad_request_list[ad.id] = [ad.name, ad.status, ad.influencer_id]
    return ad_request_list

def fetch_influencers():
    influencer = User.query.filter_by(type = 'general', is_flagged = "False" ).all()
    influencer_list = {}
    for user in influencer: 
        if user.id not in influencer_list.keys():
            influencer_list[user.id] = [user.full_name, user.category, user.niche, user.followers]
    return influencer_list

def fetch_sponsers():
    sponsers = Sponser.query.filter_by( is_flagged = "False").all()
    sponser_list = {}
    for sponser in sponsers: 
        if sponser.id not in sponser_list.keys():
            sponser_list[sponser.id] = [sponser.company_name, sponser.industry]
    return sponser_list

def fetch_flagged_user():
    flagged = User.query.filter_by(is_flagged = "True").all()
    flag_list = {}
    for user in flagged: 
        if user.id not in flag_list.keys():
            flag_list[user.id] = [user.full_name, user.email, user.category, user.followers]
    return flag_list

def fetch_flagged_sponser():
    flagged = Sponser.query.filter_by(is_flagged = "True").all()
    flag_list = {}
    for sponser in flagged: 
        if sponser.id not in flag_list.keys():
            flag_list[sponser.id] = [sponser.company_name, sponser.email, sponser.industry]
    return flag_list




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

def generate_admin_stats(campaign_id):
    pass

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
        db.session.add(campaign_obj)
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


@app.route("/edit/ad_request/<int:campaign_id>", methods = ["GET", "POST"])
def edit_ad_request(campaign_id):
    if request.method=="POST":
        ad_id = request.form.get("ad_id")
        new_ad_name=request.form.get("ad_name")
        new_terms = request.form.get("terms")
        new_status = request.form.get("status")
        new_payment = request.form.get("payment")
        new_influencer = request.form.get("influencer")
        ad_obj = Ad_request.query.filter_by(campaign_id = campaign_id, name = new_ad_name).first()
        ad_obj.name = new_ad_name
        ad_obj.requirements = new_terms
        ad_obj.status = new_status
        ad_obj.payment_amount = new_payment
        ad_obj.inlfluencer_id = new_influencer
        db.session.add(ad_obj)
        db.session.commit()
        campaign = Campaigns.query.get(campaign_id)
        campaigns = fetch_campaign_info()
        return render_template("sponser_dashboard_view_campaign.html", campaign = campaign, campaigns = campaigns)
    
@app.route("/delete/ad_request/<int:campaign_id>",methods=["GET","POST"])
def delete_ad_request(campaign_id):
    if request.method=="POST":
        ad_name=request.form.get("ad_name")
        ad_obj=Ad_request.query.filter_by(campaign_id = campaign_id, name = ad_name).first()
        db.session.delete(ad_obj)
        db.session.commit()
        campaign = Campaigns.query.get(campaign_id)
        campaigns = fetch_campaign_info()
        return render_template("sponser_dashboard_view_campaign.html", campaign = campaign, campaigns = campaigns)
    


#-------------------------------------------------------Sponser Routes-------------------------------------------------------

@app.route("/sponser/dashboard/profile/<int:s_id>", methods = ["GET", "POST"])
def sponser_dashboard_profile(s_id):
    sponser = Sponser.query.get(s_id)
    return redirect(f'/sponser/dashboard/{sponser.id}')



@app.route("/sponser/dashboard/find/<int:s_id>", methods = ["GET", "POST"])
def sponser_dashboard_find(s_id):
    sponser = Sponser.query.get(s_id)
    influencers = fetch_influencers()
    return render_template("sponser_dashboard_find.html", sponser = sponser, influencers = influencers)

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

@app.route("/influencer/dashboard/find/<int:i_id>")
def influencer_dashboard_find(i_id):
    influencer = User.query.get(i_id)
    campaign_summary = fetch_campaigns()
    return render_template("influencer_dashboard_find.html", influencer = influencer, campaigns = campaign_summary)

@app.route("/influencer/dashboard/profile/<int:i_id>")
def influencer_dashboard_profile(i_id):
    influencer = User.query.get(i_id)
    return redirect(f'/influencer/dashboard/{influencer.id}')
    


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

@app.route('/edit/profile/influencer/<int:i_id>', methods=["GET", "POST"])
def edit_influencer_profile(i_id):
    if request.method=="POST":
        new_user_name = request.form.get("uname")
        new_password = request.form.get("pwd")
        user_obj = User.query.filter_by(id = i_id, user_name = new_user_name).first()
        user_obj.user_name = new_user_name
        user_obj.pwd = new_password
        db.ssession.commit()
        user = User.query.get(i_id)
        return render_template("edit_influencer_profile.html", user_name = user.user_name, username = user.full_name)
    return render_template("influencer_dashboard_profile.html")

#-------------------------------------------------------Admin routes-------------------------------------------------------

@app.route("/admin/dashboard/info")
def admin_dashboard_info():
    campaign_summary = fetch_campaigns() 
    flagged_user = fetch_flagged_user()
    flagged_sponser = fetch_flagged_sponser()
    return render_template("admin_dashboard_info.html", campaigns = campaign_summary , flagged_user = flagged_user, flagged_sponser = flagged_sponser)

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

@app.route('/view/influencer/<int:user_id>')
def view_user(user_id):
    user = User.query.get(user_id)
    return render_template("sponser_view_influencer.html", user = user)

@app.route('/admin/view/user/<int:i_id>')
def admin_view_user(i_id):
    user = User.query.get(i_id)
    return render_template("admin_users_view.html", user=user)

@app.route('/admin/view/sponser/<int:s_id>')
def admin_view_sponser(s_id):
    sponser = Sponser.query.get(s_id)
    return render_template("admin_sponser_view.html", sponser = sponser)


#-------------------------------------------------------Flag/Remove Button Routes-------------------------------------------------------

@app.route('/flag/user/<int:i_id>')
def flag(i_id):
    user = User.query.filter_by(id = i_id).first()
    user.is_flagged = "True"
    db.session.commit()
    return redirect('/admin/dashboard/info')

@app.route('/remove/flagged/user/<int:i_id>')
def remove(i_id):
    user = User.query.filter_by(id = i_id).first()
    user.is_flagged = "False"
    db.session.commit()
    return redirect('/admin/dashboard/info')

@app.route('/flag/sponser/<int:s_id>')
def flag_sponser(s_id):
    sponser = Sponser.query.filter_by(id = s_id).first()
    sponser.is_flagged = "True"
    db.session.commit()
    return redirect('/admin/dashboard/info')

@app.route('/remove/flagged/sponser/<int:s_id>')
def remove_sponser(s_id):
    sponser = Sponser.query.filter_by(id = s_id).first()
    sponser.is_flagged = "False"
    db.session.commit()
    return redirect('/admin/dashboard/info')

#-------------------------------------------------------Stats Routes-------------------------------------------------------

@app.route('/admin/stats')
def show_admin_stats():
    campaigns = Campaigns.query.all()
    types = []
    for campaign in campaigns:
        types.append(campaign.visibility)
    plt.clf()
    plt.title("Active Campaigns")
    plt.xlabel("Type of Campaigns")
    plt.ylabel("Number of Campaigns")
    plt.hist(types, color="orange")
    plt.savefig('static/img/stats/img.png')

    influencer = User.query.filter_by(type="general").all()
    sponsor = Sponser.query.all()
    types = []
    for i in influencer:
        types.append(i.type)
    for s in sponsor:
        types.append(s.type)
    plt.clf()
    plt.title("Active Users")
    plt.xlabel("Type of User")
    plt.ylabel("Number of Users")
    plt.hist(types, color="maroon")
    plt.savefig('static/img/stats/is_img.png')

    flagged_influencer = User.query.filter_by(is_flagged = "True")
    flagged_sponsor = Sponser.query.filter_by(is_flagged = "True")
    flagged = []
    for i in flagged_influencer:
        flagged.append(i.type)
    for s in flagged_sponsor:
        flagged.append(s.type)
    plt.clf()
    plt.title("Flagged Users")
    plt.xlabel("Type of User")
    plt.ylabel("Number of flagged Users")
    plt.hist(flagged, color="green")
    plt.savefig('static/img/stats/fis_img.png')

    influencer = User.query.filter_by(type="general").all()
    types = []
    for i in influencer:
        types.append(i.niche)
    plt.clf()
    plt.title("Influencers based on Niche")
    plt.xlabel("Niche")
    plt.ylabel("Number of Influencers")
    plt.hist(types, color="blue")
    plt.savefig('static/img/stats/iimg.png')

    sponser = Sponser.query.all()
    types = []
    for s in sponser:
        types.append(s.industry)
    plt.clf()
    plt.title("Sponors based on Industry")
    plt.xlabel("Industry")
    plt.ylabel("Number of Sponsors")
    plt.hist(types, color="yellow")
    plt.savefig('static/img/stats/simg.png')

    ad = Ad_request.query.all()
    types = []
    for a in ad:
        types.append(a.status)
    plt.clf()
    plt.title("Ad Requests")
    plt.xlabel("Ad-Requests")
    plt.ylabel("Number of Ads")
    plt.hist(types)
    plt.savefig('static/img/stats/aimg.png')

    
    return render_template("admin_stats.html")


@app.route('/influencer/stats')
def show_influencer_stats():
    campaigns = Campaigns.query.all()
    types = []
    for campaign in campaigns:
        types.append(campaign.niche)
    plt.clf()
    plt.title("Campaigns based on Niche")
    plt.xlabel("Type of Campaigns")
    plt.ylabel("Number of Campaigns")
    plt.hist(types, color="maroon")
    plt.savefig('static/img/stats/influencer_img.png')

    campaigns = Campaigns.query.all()
    types = []
    for campaign in campaigns:
        types.append(campaign.visibility)
    plt.clf()
    plt.title("Active Campaigns")
    plt.xlabel("Type of Campaigns")
    plt.ylabel("Number of Campaigns")
    plt.hist(types)
    plt.savefig('static/img/stats/cimg.png')

    return render_template("influencer_stats.html")



   
@app.route('/sponser/stats')
def show_sponser_stats():
    influencer = User.query.filter_by(type="general").all()
    types = []
    for i in influencer:
        types.append(i.niche)
    plt.clf()
    plt.title("Influencers based on Niche")
    plt.xlabel("Niche")
    plt.ylabel("Number of Influencers")
    plt.hist(types, color="green")
    plt.savefig('static/img/stats/sponser_img.png')

    influencers = User.query.filter_by(type="general").all()
    types = []
    for i in influencers:
        types.append(i.followers)
    plt.clf()
    plt.title("Influencers based on Followers")
    plt.xlabel("Followers")
    plt.ylabel("Number of Influencers")
    plt.hist(types, ec="red")
    plt.savefig('static/img/stats/fimg.png')
    
    return render_template("sponser_stats.html")

#-------------------------------------------------------Request button Routes Influencer to Sponser-------------------------------------------------------

@app.route('/send/request/<int:i_id>', methods=["GET", "POST"])
def send(i_id):
    if request.method == "POST":
        influencer = User.query.get(i_id)
        campaign_id = request.form.get("campaign_id")
        influencer_id = request.form.get("influencer_id")
        sponser_id = request.form.get("sponser_id")
        new_request = Influencer_Request(influencer_id = influencer_id, sponser_id = sponser_id, campaign_id = campaign_id)
        db.session.add(new_request)
        db.session.commit()
        print("Request sent successfully!")
        return redirect(f'/influencer/dashboard/find/{influencer.id}')
    
@app.route('/accept/request/<int:s_id>' , methods = ["GET" , "POST"])
def accept(s_id):
    if request.method == "POST":
        sponser = Sponser.query.get(s_id)
        request_id = request.form.get("request_id")
        req_obj = Influencer_Request.query.filter_by(id=request_id).first()
        req_obj.status = "Accepted"
        db.session.commit()
        return redirect(f'/sponser/dashboard/{sponser.id}')

@app.route('/reject/request/<int:s_id>' , methods = ["GET" , "POST"])
def reject(s_id):
    if request.method == "POST":
        sponser = Sponser.query.get(s_id)
        request_id = request.form.get("request_id")
        req_obj = Influencer_Request.query.filter_by(id=request_id).first()
        req_obj.status = "Rejected"
        db.session.commit()
        return redirect(f'/sponser/dashboard/{sponser.id}')
    

#-----------------------------------------------------Request button Routes Sponser to Influencer-------------------------------------------------------

@app.route('/request/influencer/<int:s_id>/<int:i_id>')
def request_influencer(s_id, i_id):
    influencer = User.query.get(i_id)
    sponser = Sponser.query.get(s_id)
    private_campaigns = Campaigns.query.filter_by(sponser_id = s_id, visibility = "Private")
    ad_request = fetch_ad_requests()
    return render_template("sponser_private_campaigns.html", private_campaigns = private_campaigns, ad_request = ad_request, influencer=influencer, sponser=sponser)


@app.route('/send/request/influencer/<int:s_id>' , methods = ["GET", "POST"])
def send_request_influencer(s_id):
    if request.method=="POST":
        sponser = Sponser.query.get(s_id)
        campaign_id = request.form.get("campaign_id")
        sponser_id = request.form.get("sponser_id")
        influencer_id = request.form.get("influencer_id")
        new_request = Sponser_Request(influencer_id = influencer_id, sponser_id = sponser_id, campaign_id = campaign_id)
        db.session.add(new_request)
        db.session.commit()
        print("Request sent successfully!")
        return redirect(f'/sponser/dashboard/find/{sponser.id}')
    
@app.route('/accept/sponser/request/<int:i_id>' , methods = ["GET" , "POST"])
def accept_request(i_id):
    if request.method == "POST":
        influencer = User.query.get(i_id)
        request_id = request.form.get("request_id")
        req_obj = Sponser_Request.query.filter_by(id=request_id).first()
        req_obj.status = "Accepted"
        db.session.commit()
        return redirect(f'/influencer/dashboard/{influencer.id}')

@app.route('/reject/sponser/request/<int:i_id>' , methods = ["GET" , "POST"])
def reject_request(i_id):
    if request.method == "POST":
        influencer = User.query.get(i_id)
        request_id = request.form.get("request_id")
        req_obj = Sponser_Request.query.filter_by(id=request_id).first()
        req_obj.status = "Rejected"
        db.session.commit()
        return redirect(f'/influencer/dashboard/{influencer.id}')
    
@app.route('/view/ad/<int:campaign_id>')
def view_ad(campaign_id):
    ads = Ad_request.query.filter_by(campaign_id = campaign_id).all()
    return render_template("view_ad.html", ads = ads)

#-----------------------------------------------------Accept/Reject button Routes for Ads-------------------------------------------------------

@app.route('/reject/ad/<int:a_id>', methods=["POST"])
def reject_ad(a_id):
    if request.method=="POST":
        ad = Ad_request.query.get(a_id)
        ad_id = request.form.get("ad_id")
        ad_obj = Ad_request.query.filter_by(id = ad_id).first()
        ad_obj.status = "Rejected"
        db.session.commit()
        return redirect(f'/influencer/dashboard/{ad.influencer_id}')
    
@app.route('/accept/ad/<int:a_id>', methods=["POST"])
def accept_ad(a_id):
    if request.method=="POST":
        ad = Ad_request.query.get(a_id)
        ad_id = request.form.get("ad_id")
        ad_obj = Ad_request.query.filter_by(id = ad_id).first()
        ad_obj.status = "Accepted"
        db.session.commit()
        return redirect(f'/influencer/dashboard/{ad.influencer_id}')
    















