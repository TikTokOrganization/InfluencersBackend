import flask, json, pickle
import YTShortsCategorizer, LikedShortsGetter


LOGIN_URI = "http://localhost:8080/login"


app = flask.Flask(__name__)
ytShortsGetter = YTShortsCategorizer.YoutubeShortsGetter()


@app.route("/")
def index():
    return "<h1>Influencers Backend</h1>"

@app.route("/login")
def login():
    auth_filepath = LikedShortsGetter.get_config_filepath()
    auth_info = LikedShortsGetter.load_auth_info(auth_filepath)
    auth_info["redirect_uri"] = LOGIN_URI
    
    if "code" not in flask.request.args:
        print("Requesting auth...")
        return flask.redirect(LikedShortsGetter.get_oauth_url(auth_info))
    else:
        print("Requesting token...")
        auth_code = flask.request.args.get("code")
        oauth_token = LikedShortsGetter.get_oauth_token(auth_info, auth_code)
        print(f"Oauth Token: {oauth_token}")
        
        tokens = {auth_info["client_id"]: oauth_token}
        with open("oauth_tokens.txt", "wb") as output_file:
            pickle.dump(tokens, output_file)
        
        return flask.redirect(flask.url_for("index"))

@app.route("/getLikedShorts")
def get_liked_shorts():
    try:
        client_id = flask.request.args.get("client_id")
        print(f"Client ID: {client_id}")
        with open("oauth_tokens.txt", "rb") as input_file:
            tokens = pickle.load(input_file)
            oauth_token = tokens[client_id]
        print(f"Token: {oauth_token}")
        
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
        shorts = ytShortsGetter.getShortsOfCategory(category)
        return_val = {"shorts": shorts}
    except Exception as e:
        print(f"Error: {e}")
        return_val = flask.Response(status = 500)
    
    return return_val


if __name__ == "__main__":
    app.secret_key = "SUPER_SECRET" #Change later
    app.run("localhost", 8080, debug = True)  