import flask, json, pickle
import YTShortsCategorizer, LikedShortsGetter
import google.oauth2.credentials
import google_auth_oauthlib.flow
import youtubeShortsGetter
from elasticsearch import Elasticsearch
import os


LOGIN_URI = "http://localhost:8080/login"


app = flask.Flask(__name__)
ytShortsGetter = youtubeShortsGetter.youtubeShortsGetter()
es = ytShortsGetter.initializeElasticIndex()


@app.route("/")
def index():
    return "<h1>Influencers Backend</h1>"

@app.route("/login")
def login():
    #auth_filepath = LikedShortsGetter.get_config_filepath()
    #auth_info = LikedShortsGetter.load_auth_info(auth_filepath)
    #auth_info["redirect_uri"] = LOGIN_URI
    #
    #if "code" not in flask.request.args:
    #    print("Requesting auth...")
    #    return flask.redirect(LikedShortsGetter.get_oauth_url(auth_info))
    #else:
    #    print("Requesting token...")
    #    auth_code = flask.request.args.get("code")
    #    oauth_token = LikedShortsGetter.get_oauth_token(auth_info, auth_code)
    #    print(f"Oauth Token: {oauth_token}")
    #    
    #    tokens = {auth_info["client_id"]: oauth_token}
    #    with open("oauth_tokens.txt", "wb") as output_file:
    #        pickle.dump(tokens, output_file)
    #    
    #    return flask.redirect(flask.url_for("index"))

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'config/client_secret.json', 
        scopes = "https://www.googleapis.com/auth/youtube.readonly")
    
    flow.redirect_uri = "http://localhost:8080/oauth2callback"
    
    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true')
    flask.session['state'] = state

    return flask.redirect(authorization_url)

@app.route("/oauth2callback")
def oauth2callback():
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'config/client_secret.json', 
        scopes = "https://www.googleapis.com/auth/youtube.readonly",
        state = state)
    
    flow.redirect_uri = "http://localhost:8080/oauth2callback"

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response = authorization_response)

    credentials = flow.credentials
    flask.session['credentials'] = {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

    return flask.redirect("http://localhost:8080/")

@app.route("/getLikedShorts")
def get_liked_shorts():
    try:
        #client_id = flask.request.args.get("client_id")
        #print(f"Client ID: {client_id}")
        #with open("oauth_tokens.txt", "rb") as input_file:
        #    tokens = pickle.load(input_file)
        #    oauth_token = tokens[client_id]
        #print(f"Token: {oauth_token}")
        #

        oauth_token = (flask.session['credentials'])['token']
        print("Making search request...")
        LikedShortsGetter.get_liked_videos(oauth_token, "finalOutput.json")

        status_code = 200
    except Exception as e:
        print(f"Error: {e}")
        status_code = 500
    
    return flask.Response(status = status_code)

@app.route("/getCategories")
def get_categories():
    return ytShortsGetter.getCategories()

@app.route("/getShortsOfCategory")
def get_shorts_of_category():
    try:
        category = int(flask.request.args.get("category"))
        shorts = ytShortsGetter.getShortsOfCategory(category, es)
        return_val = {"shorts": shorts}
    except Exception as e:
        print(f"Error: {e}")
        return_val = flask.Response(status = 500)
    
    return return_val

@app.route("/initializeElastic")
def initialize_Elastic():
    flask.session['es'] = ytShortsGetter.initializeElasticIndex()
    return flask.redirect("http://localhost:8080/")

@app.route("/moreLikeThis")
def more_like_this():
    keyword = flask.request.args.get("keyword")
    return ytShortsGetter.getMoreLikeThis(keyword, es)


if __name__ == "__main__":
    app.secret_key = "SUPER_SECRET" #Change later
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run("localhost", 8080, debug = True)  