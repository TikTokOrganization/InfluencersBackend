from requests import post
from datetime import datetime, timezone
from src.media_retriever import MediaRetriever
from flask import Flask, redirect, render_template, request, session, Response


app = Flask(__name__)
app.secret_key = "secret_key"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/badLanding")
def bad_landing():
    return render_template("bad-landing.html")

@app.post("/login")
def login():
    if "code" in request.form.keys():
        session["token"] = request.form["code"]
        session["last_updated_token"] = datetime.now(tz = timezone.utc)
        return Response(status = 200)
    else:
        return Response(status = 404)

@app.route("/logOut")
def log_out():
    if "token" in session.keys():
        del session["token"]
        del session["last_updated_token"]
        return Response(status = 200)
    else:
        return Response(status = 400)

@app.post("/getData")
def get_data():
    if not "refresh" in request.form.keys():
        return "Bad request, send refresh flag."
    
    global session_start
    if "failsafe" in session.keys():
        failsafe = session["failsafe"] and session["last_updated_failsafe"] > session_start
    else:
        failsafe = True

    if request.form["refresh"] == "0":
        data = mediaRetriever.get_content(refresh = False, failsafe = failsafe)
    else:
        print("Refresh indicated.")
        data = mediaRetriever.get_content(refresh = True, failsafe = failsafe)

    return data

@app.route("/oauth2callback")
def dash():
    if not "token" in session.keys() or not "last_updated_token" in session.keys():
        return redirect("badLanding")
    
    #Check to see if the token was from a previous session
    global session_start
    if session["last_updated_token"] < session_start:
        return redirect("badLanding")

    payload = {
        "client_id": "620677125812-g4634rpb7kam1r5hm8kq2mdccdhg3i5l.apps.googleusercontent.com",
        "client_secret": "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",
        "code": session["token"],
        "grant_type": "authorization_code",
        "redirect_uri": "postmessage"
    }
    token_response = post("https://oauth2.googleapis.com/token", data = payload)
    if token_response.status_code == 200:
        session["failsafe"] = False
        session["last_updated_failsafe"] = datetime.now(tz = timezone.utc)
        mediaRetriever.update_source(token_response.json()["access_token"])
    else:
        session["failsafe"] = True
        session["last_updated_failsafe"] = datetime.now(tz = timezone.utc)
    
    return render_template("shorts-viewer.html")

if __name__ == "__main__":
    mediaRetriever = MediaRetriever("failsafe.json")

    session_start = datetime.now(tz = timezone.utc)

    app.run("localhost", 8080, debug = True)