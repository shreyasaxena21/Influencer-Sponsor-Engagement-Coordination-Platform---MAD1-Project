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

class Sponser_Info(db.Model):
    __tablename__="sponser_info"
    s_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    user_name = db.Column(db.String, unique=True, nullable=False)
    pwd = db.Column(db.String, nullable=False)
    industry = db.Column(db.String, nullable=False)
    company_name = db.Column(db.String, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Influencer_Info(db.Model):
    __tablename__="influencer_info"
    i_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    user_name = db.Column(db.String, unique=True, nullable=False)
    pwd = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    niche = db.Column(db.String, nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Campaign(db.Model):
    __tablename__="campaign"
    campaign_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, default=datetime.utcnow())
    end_date = db.Column(db.Date, default=None)
    budget = db.Column(db.Integer, nullable= False)
    visibility = db.Column(db.String, default="public")
    goals = db.Column(db.String, nullable=False)

class Ad_Request(db.Model):
    __tablename__="ad_request"
    messages = db.Column(db.String, nullable=False)
    requirements = db.Column(db.String, nullable=False)
    payment_amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
