from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy() #Instance of SQLALchemy

class Admin_Info(db.Model):
    __tablename__="admin_info"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    user_name = db.Column(db.String, unique=True, nullable=False)
    pwd = db.Column(db.String, nullable=False)
    is_admin= db.Column(db.Boolean, default=True)

class Influencer_Info(db.Model):
    __tablename__ = "influencer_info"
    influencer_id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String, nullable=False)
    user_name = db.Column(db.String, nullable=False)
    pwd = db.Column(db.String, nullable=False)
    name  = db.Column(db.String, nullable=False)
    niche = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    is_influencer = db.Column(db.Boolean, default=True)



class Sponser_Info(db.Model):
    __tablename__="sponser_info"
    sponser_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    user_name = db.Column(db.String, unique=True, nullable=False)
    pwd = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    industry = db.Column(db.String, nullable=False)
    company_name = db.Column(db.String, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    is_sponser = db.Column(db.Boolean, default=True)



class Campaigns(db.Model):
    __tablename__ = "campaigns"
    camp_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)


class Ad_Request(db.Model):
    __tablename__ = "ad_request"
    ad_id = db.Column(db.Integer, primary_key=True)
    messages = db.Column(db.String, nullable=False)
    requirements = db.Column(db.String, nullable=False)
    payment_amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    camp_id = db.Column(db.Integer, db.ForeignKey("campaigns.camp_id"), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey("influencer_info.influencer_id"), nullable=False)
    campaigns = db.relationship("Campaigns", foreign_keys="campaigns.camp_id")
    influencer_info = db.relationship("Influencer_Info", foreign_keys="influencer_info.influencer_id")


class Goals(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    camp_description = db.Column(db.String, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    visibility = db.Column(db.String, nullable=False, default="public")
    goals = db.Column(db.String, nullable=False)
    camp_id = db.Column(db.Integer, db.ForeignKey("campaigns.camp_id"), nullable=False)
    ad_id = db.Column(db.Integer, db.ForeignKey("ad_request.ad_id"), nullable=False)
    campaigns = db.relationship("Campaigns", foreign_keys="campaigns.camp_id")
    ad_request = db.relationship("Ad_Request", foreign_keys="ad_request.ad_id")


class Create_Campaign(db.Model):
    __tablename__ = "create_campaign"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    niche = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable = False)
    camp_id = db.Column(db.Integer, db.ForeignKey("campaigns.camp_id"), nullable=False)
    sponser_id = db.Column(db.Integer, db.ForeignKey("sponser_info.sponser_id"), nullable=False)
    campaigns = db.relationship("Campaigns", foreign_keys="campaigns.camp_id")
    sponser_info = db.relationship("Sponser_Info", foreign_keys="ad_request.ad_id")




    



