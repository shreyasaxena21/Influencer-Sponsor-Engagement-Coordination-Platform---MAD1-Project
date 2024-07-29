from flask_restful import Api,Resource,reqparse
from .models import *

api=Api()

#----------------------------------------------------Parser for Influencers----------------------------------------------------
influencer_parser = reqparse.RequestParser()
influencer_parser.add_argument("email")
influencer_parser.add_argument("fullname")
influencer_parser.add_argument("uname")
influencer_parser.add_argument("category")
influencer_parser.add_argument("niche")
influencer_parser.add_argument("followers")

class InfluencerApi(Resource):

    def get(self, i_id):
        influencers = User.query.filter_by(id = i_id).all()
        influencer_list = []
        for influencer in influencers:
            influencer_details={}
            influencer_details["id"] = influencer.id
            influencer_details["email"] = influencer.email
            influencer_details["fullname"] = influencer.full_name
            influencer_details["uname"] = influencer.user_name
            influencer_details["category"] = influencer.category
            influencer_details["niche"] = influencer.niche
            influencer_details["followers"] = influencer.followers
            influencer_list.append(influencer_details)
        return influencer_list
    
    def post(self, i_id):
        influencer_data = influencer_parser.parse_args()
        new_influencer = User(id=i_id, email =influencer_data["email"], full_name = influencer_data["fullname"], user_name = influencer_data["uname"], category = influencer_data["category"], niche = influencer_data["niche"], followers = influencer_data["followers"])
        db.session.add(new_influencer)
        db.session.commit()
        return "Influencer is created successfully!",201

    def put(self, i_id):
        influencer_data = influencer_parser.parse_args()
        influencer = User.query.filter_by(id = i_id).first()
        if influencer:
            influencer.email = influencer_data["email"]
            influencer.full_name = influencer_data["fullname"]
            influencer.user_name = influencer_data["uname"]
            influencer.category = influencer_data["category"]
            influencer.niche = influencer_data["niche"]
            influencer.followers = influencer_data["followers"]
            db.session.commit()
            return "Influencer details are updated!",200
        else:
            return "Influencer not found!",400

    def delete(self, i_id):
        influencer = User.query.filter_by(id = i_id).first()
        if influencer:
            db.session.delete(influencer)
            db.session.commit()
            return "Influencer is deleted successfully!",200
        else:
            return "Influencer not found!",400
        
api.add_resource(InfluencerApi,"/api/influencer/<int:i_id>")


#----------------------------------------------------Parser for Sponsers----------------------------------------------------
sponser_parser = reqparse.RequestParser()
sponser_parser.add_argument("email")
sponser_parser.add_argument("company_name")
sponser_parser.add_argument("uname")
sponser_parser.add_argument("industry")

class SponserApi(Resource):

    def get(self, s_id):
        sponsers = Sponser.query.filter_by(id = s_id).all()
        sponser_list = []
        for sponser in sponsers:
            sponser_details={}
            sponser_details["id"] = sponser.id
            sponser_details["email"] = sponser.email
            sponser_details["company_name"] = sponser.company_name
            sponser_details["uname"] = sponser.user_name
            sponser_details["industry"] = sponser.industry
            sponser_list.append(sponser_details)
        return sponser_list
    
    def post(self, s_id):
        sponser_data = sponser_parser.parse_args()
        new_sponser = Sponser(id=s_id, email =sponser_data["email"], company_name = sponser_data["company_name"], user_name = sponser_data["uname"], industry = sponser_data["industry"])
        db.session.add(new_sponser)
        db.session.commit()
        return "Sponsor is created successfully!",201

    def put(self, s_id):
        sponser_data = sponser_parser.parse_args()
        sponser = Sponser.query.filter_by(id = s_id).first()
        if sponser:
            sponser.email = sponser_data["email"]
            sponser.company_name = sponser_data["company_name"]
            sponser.user_name = sponser_data["uname"]
            sponser.industry = sponser_data["industry"]
            db.session.commit()
            return "Sponsor details are updated!",200
        else:
            return "Sponsor not found!",400

    def delete(self, s_id):
        sponser = Sponser.query.filter_by(id = s_id).first()
        if sponser:
            db.session.delete(sponser)
            db.session.commit()
            return "Sponsor is deleted successfully!",200
        else:
            return "Sponsor not found!",400
        
api.add_resource(SponserApi,"/api/sponser/<int:s_id>")

#----------------------------------------------------Parser for Campaigns----------------------------------------------------
campaign_parser=reqparse.RequestParser()
campaign_parser.add_argument("title")
campaign_parser.add_argument("description")
campaign_parser.add_argument("end_date")
campaign_parser.add_argument("budget")
campaign_parser.add_argument("goals")

class CampaignApi(Resource):

    def get(self, sponser_id):
        campaigns = Campaigns.query.filter_by(sponser_id = sponser_id).all()
        sponser_list = []
        for campaign in campaigns:
            campaign_details={}
            campaign_details["id"] = campaign.id
            campaign_details["title"] = campaign.name
            campaign_details["description"] = campaign.description
            campaign_details["end_date"] = campaign.end_date
            campaign_details["budget"] = campaign.budget
            campaign_details["goals"] = campaign.goals
            sponser_list.append(campaign_details)
        return sponser_list

    def post(self, sponser_id):
        campaign_data = campaign_parser.parse_args()
        new_campaign = Campaigns(name = campaign_data["title"], description = campaign_data["description"], end_date = campaign_data["end_date"], budget = campaign_data["budget"], goals = campaign_data["goals"], sponser_id = sponser_id)
        db.session.add(new_campaign)
        db.session.commit()
        return "Campaign is created!",201

    def put(self, campaign_id):
        campaign_data = campaign_parser.parse_args()
        campaign = Campaigns.query.filter_by(id = campaign_id).first()
        if campaign:
            campaign.name = campaign_data["title"]
            campaign.description = campaign_data["description"]
            campaign.end_date = campaign_data["end_date"]
            campaign.budget = campaign_data["budget"]
            campaign.goals = campaign_data["goals"]
            db.session.commit()
            return "Campaign is updated!",200
        else:
            return "Campaign not found!",400

    def delete(self, campaign_id):
        campaign = Campaigns.query.filter_by(id = campaign_id).first()
        if campaign:
            db.session.delete(campaign)
            db.session.commit()
            return "Campaign is deleted!",200
        else:
            return "Campaign not found!",400

api.add_resource(CampaignApi,"/api/campaigns/<int:sponser_id>","/api/campaigns/update/<int:campaign_id>","/api/campaigns/delete/<int:campaign_id>" )
