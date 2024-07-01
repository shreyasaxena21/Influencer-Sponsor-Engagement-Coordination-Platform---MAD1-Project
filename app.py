from flask import Flask
from backend.models import *

app = None #initially none

def init_app():
    app = Flask(__name__) #object of Flask
    app.debug = True 
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///influencer_sponser.sqlite3"
    app.app_context().push() #direct access app, to database modules
    db.init_app(app)#object.method(parameter) init_app belongs to db object
    print("The application started....")
    return app

app=init_app()
from backend.controllers import *
if __name__ == "__main__":
    app.run()