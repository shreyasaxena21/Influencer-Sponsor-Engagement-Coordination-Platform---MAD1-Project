from flask import Flask, render_template
from flask import current_app as app #Alias for current running app

@app.route("/")#refers base url 127.0.0.1.5000 local host
def home():
    return "<h2> Welcome to Influencer - Sponser Coordination Platform </h2>"

@app.route("/login") #it refers base url and login
def user_login():
    return render_template("login.html")

@app.route("/influencer_signup") 
def influencer_signup():
    return render_template("influencer.html")

@app.route("/sponser_signup") 
def sponser_signup():
    return render_template("sponser.html")


