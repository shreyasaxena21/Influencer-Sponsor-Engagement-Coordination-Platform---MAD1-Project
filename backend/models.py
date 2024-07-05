from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy() #Instance of SQLALchemy

class Admin(db.Model):
    __tablename__="admin"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    user_name = db.Column(db.String(32), unique=True, nullable=False)
    pass_hash = db.Column(db.String(512), nullable=False)
    is_admin= db.Column(db.Boolean, default=True)

class Influencer(db.Model):
    __tablename__ = "influencer"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(32), nullable=False)
    pass_hash = db.Column(db.String(512), nullable=False)
    name  = db.Column(db.String(64), nullable=False)
    niche = db.Column(db.String(64), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    is_influencer = db.Column(db.Boolean, default=True)



class Sponser(db.Model):
    __tablename__="sponser"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(32), unique=True, nullable=False)
    pass_hash = db.Column(db.String(512), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    industry = db.Column(db.String(64), nullable=False)
    company_name = db.Column(db.String(64), nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    is_sponser = db.Column(db.Boolean, default=True)



class Campaigns(db.Model):
    __tablename__ = "campaigns"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    

class Create_Campaign(db.Model):
    __tablename__ = "create_campaign"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    niche = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable = False)
    camp_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"), nullable=False)
    sponser_id = db.Column(db.Integer, db.ForeignKey("sponser.id"), nullable=False)
    campaigns = db.relationship("Campaigns", backref="create_campaign")
    sponser = db.relationship("Sponser", backref="create_campaign")


class Ad_Request(db.Model):
    __tablename__ = "ad_request"
    id = db.Column(db.Integer, primary_key=True)
    messages = db.Column(db.String, nullable=False)
    requirements = db.Column(db.String, nullable=False)
    payment_amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    camp_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey("influencer.id"), nullable=False)
    campaigns = db.relationship("Campaigns", backref='ad_request')
    influencer = db.relationship("Influencer", backref="ad_request")


class Goals(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    camp_description = db.Column(db.String, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    visibility = db.Column(db.String, nullable=False, default="public")
    goals = db.Column(db.String, nullable=False)
    camp_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"), nullable=False)
    ad_id = db.Column(db.Integer, db.ForeignKey("ad_request.id"), nullable=False)
    campaigns = db.relationship("Campaigns", backref="goals")
    ad_request = db.relationship("Ad_Request", backref="goals")







    



