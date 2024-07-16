from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy() #Instance of SQLALchemy

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
    email = db.Column(db.String)
    full_name = db.Column(db.String, nullable = False)
    user_name = db.Column(db.String, unique = True, nullable = False)
    pwd = db.Column(db.String, nullable = False)
    category = db.Column(db.String, nullable = False, default="null")
    niche = db.Column(db.String, nullable = False, default="null")
    type = db.Column(db.String, nullable = False, default = "general")
    ad_request = db.relationship("Ad_request", backref="user")

class Sponser(db.Model):
    __tablename__ = "sponser"
    id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
    email = db.Column(db.String, nullable = False)
    company_name = db.Column(db.String, nullable = False)
    user_name = db.Column(db.String, unique = True, nullable = False)
    pwd = db.Column(db.String, nullable = False)
    industry = db.Column(db.String, nullable = False)
    budget = db.Column(db.Float, nullable = False, default = 1000.0)
    campaign = db.relationship("Campaigns", backref="sponser")

class Campaigns(db.Model):
    __tablename__ = "campaigns"
    id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.Text, nullable = False)
    start_date = db.Column(db.Date, nullable = False)
    end_date = db.Column(db.Date, nullable = False)
    budget = db.Column(db.Float, nullable = False)
    visibility = db.Column(db.String, nullable = False, default="public") 
    goals = db.Column(db.Text, nullable = False)
    niche = db.Column(db.Text, nullable = False, default = "null")
    sponser_id = db.Column(db.Integer, db.ForeignKey('sponser.id'))
    ad_request = db.relationship("Ad_request", backref="campaigns")


class Ad_request(db.Model):
    __tablename__ = "ad_request"
    id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
    message =  db.Column(db.Text, nullable = False)
    payment_amount = db.Column(db.Float, nullable = False)
    requirements = db.Column(db.String, nullable = False)
    status = db.Column(db.String, nullable = False, default = "Pending")
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'))
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.id'))



