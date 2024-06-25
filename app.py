from flask import Flask

app = None #initially none

def init_app():
    app = Flask(__name__) #object of Flask
    app.debug = True 
    app.app_context().push() #direct access app, to database modules
    print("The application started....")
    return app

app=init_app()
from backend.controllers import *
if __name__ == "__main__":
    app.run()