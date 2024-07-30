from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db=SQLAlchemy() #Instance of SQLALchemy

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
    email = db.Column(db.String, nullable = False)
    full_name = db.Column(db.String, nullable = False)
    search_name = db.Column(db.String, nullable = False, default="null")
    user_name = db.Column(db.String, unique = True, nullable = False)
    pwd = db.Column(db.String, nullable = False, default="null")
    category = db.Column(db.String, nullable = False, default="null")
    niche = db.Column(db.String, nullable = False, default="null")
    followers = db.Column(db.Integer, nullable=False, default = 0)
    type = db.Column(db.String, nullable = False, default = "general")
    is_flagged = db.Column(db.String, nullable=False, default="False")
    ad_request = db.relationship("Ad_request", cascade="all, delete", backref="user")



class Sponser(db.Model):
    __tablename__ = "sponser"
    id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
    email = db.Column(db.String, nullable = False)
    company_name = db.Column(db.String, nullable = False)
    search_name = db.Column(db.String, nullable = False, default="null")
    user_name = db.Column(db.String, unique = True, nullable = False)
    pwd = db.Column(db.String, nullable = False,  default="null")
    industry = db.Column(db.String, nullable = False)
    budget = db.Column(db.Float, nullable = False, default = 1000.0)
    is_flagged = db.Column(db.String, nullable=False, default="False")
    type = db.Column(db.String, nullable = False, default = "Sponsor")
    campaigns = db.relationship("Campaigns", cascade="all, delete", backref="sponser")

class Campaigns(db.Model):
    __tablename__ = "campaigns"
    id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    search_name = db.Column(db.String, nullable = False, default = "null")
    description = db.Column(db.Text, nullable = False)
    start_date = db.Column(db.String, nullable = False, default = "null")
    end_date = db.Column(db.String, nullable = False)
    budget = db.Column(db.Float, nullable = False)
    visibility = db.Column(db.String, nullable = False, default="public") 
    goals = db.Column(db.Text, nullable = False)
    niche = db.Column(db.Text, nullable = False, default = "null")
    sponser_id = db.Column(db.Integer, db.ForeignKey("sponser.id"), nullable = False)
    ad_requests = db.relationship("Ad_request", cascade="all, delete", backref="campaigns")


class Ad_request(db.Model):
    __tablename__ = "ad_request"
    id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
    name =  db.Column(db.Text, nullable = False)
    message =  db.Column(db.Text, nullable = False)
    payment_amount = db.Column(db.Float, nullable = False)
    requirements = db.Column(db.String, nullable = False)
    status = db.Column(db.String, nullable = False, default = "Pending")
    visibility = db.Column(db.String, nullable = False, default="Public") 
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"), nullable = False)
    influencer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)

class Influencer_Request(db.Model):     #Table for the requests sent by influencers to sponsers
    __tablename__="influencer_request" 
    id = db.Column(db.Integer, primary_key=True,  nullable = False, autoincrement = True)
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sponser_id = db.Column(db.Integer, db.ForeignKey('sponser.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')

    influencer = db.relationship('User', backref='influencer_request')
    sponser = db.relationship('Sponser', backref='influencer_request')
    campaign = db.relationship('Campaigns', backref='influencer_request')

class Sponser_Request(db.Model):     #Table for the requests sent by sponsers to influencer
    __tablename__="sponser_request" 
    id = db.Column(db.Integer, primary_key=True,  nullable = False, autoincrement = True)
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sponser_id = db.Column(db.Integer, db.ForeignKey('sponser.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')

    influencer = db.relationship('User', backref='sponser_request')
    sponser = db.relationship('Sponser', backref='sponser_request')
    campaign = db.relationship('Campaigns', backref='sponser_request')

