import requests, logging
from json import dump, load, loads, dumps
from os import path, mkdir, listdir
from sys import exit
import google.oauth2.credentials
import google_auth_oauthlib.flow


SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

#Ensure config file exists
def get_config_filepath() -> str:
    """Validate config/auth.json exists. If so, return path to file. If not exit program."""

    if not path.isdir("config"):
        logging.error("Config folder does not exist. Please pull the latest stable branch.")
        exit(0)
    config_filepath = path.join("config", "auth.json")
    if not path.isfile(config_filepath):
        logging.error(f"Auth file at {config_filepath} does not exist. Please pull the latest stable branch.")
        exit(0)
    
    return config_filepath


def load_auth_info(auth_filepath: str) -> str:
    """Get authorization credentials from config/auth.json file."""

    with open(auth_filepath) as auth_file:
        auth_info = load(auth_file)
    
    return auth_info


def get_oauth_url(auth_info: dict) -> str:
    """Generate query url to Google Auth API to authenticate user."""

    #auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
#
    #auth_info = dict(auth_info)
    #del auth_info["client_secret"]
    #auth_info["response_type"] = "code"
    #auth_info["scope"] = " ".join(SCOPES)
    #auth_info["access_type"] = "offline"
    ##auth_info["state"] = "RANDOM_STATE" #Replace later
#
    #r = requests.Request("GET", auth_url, params = auth_info).prepare()
    

    #return r.url


def get_oauth_token(token_params: dict, auth_code: str) -> str:
    """Generate query url to Google API to request an OAuth 2.0 token"""

    token_url = "https://accounts.google.com/o/oauth2/token"

    token_params["code"] = auth_code
    token_params["grant_type"] = "authorization_code"

    token_request = requests.post(token_url, data = token_params)
    token_request_data = loads(token_request.text)


    return token_request_data["access_token"]


def get_liked_videos(oauth_token: str, output_filepath: str) -> None:
    """Make search request to Youtube API for liked videos on a user's profile"""

    query_url = "https://youtube.googleapis.com/youtube/v3/videos"

    auth_headers = {"Authorization": f"Bearer {oauth_token}"}
    search_params = {
        "myRating": "like",
        "key": "AIzaSyBEDqAaPKfAOqKvw8EjTLlI7A4JE1cmR9M",
        "part": "snippet,contentDetails,statistics",
    }

    print("Sending search query...")
    try:
        search_response = requests.get(query_url, headers = auth_headers, params = search_params)
        print(f"Search Response Status Code: {search_response.status_code}")
        search_response = loads(search_response.text)

        items = []
        items.extend(search_response["items"])

        while 'nextPageToken' in search_response:
            nextPageToken = search_response['nextPageToken']
            search_params['pageToken'] = nextPageToken

            search_response = requests.get(query_url, headers = auth_headers, params = search_params)
            print(f"Search Response Status Code: {search_response.status_code}")
            search_response = loads(search_response.text)

            items.extend(search_response["items"])
        
        print(dumps(items, indent=4))

        shorts = {"items": []}
        for video in items:
            videoID = video["id"]
            shortsURL = "https://yt.lemnoslife.com/videos"
            shortsParams = {"part": "short",
                            "id": videoID}
            shortTestResponse = requests.get(shortsURL, params = shortsParams)
            shortTestResponse = loads(shortTestResponse.text)

            if shortTestResponse["items"][0]["short"]["available"] is True:
                shorts["items"].append(video)
            
        with open(output_filepath, "w") as output_file:
            dump(shorts, output_file)
        
        print(f"Finished writing {output_filepath}")
    except Exception as e:
        print(f"Request exception, error: {e}")


#Set up logger
def logfile_setup() -> str:
    """Generate path to logfile."""

    if not path.isdir("logs"):
        mkdir("logs")
    filename = f"log-{len(listdir('logs'))}"
    
    return path.join("logs", filename)


def main() -> None:
    logging.info("Loading authorization credentials...")
    auth_filepath = get_config_filepath()
    auth_info = load_auth_info(auth_filepath)
    logging.info("Authorization info loaded.")

    logging.info("Attempting request...")
    user_data = get_liked_videos(auth_info)
    logging.info("Request completed.")

    logging.info("Writing data to file...")
    with open("search_data.json") as output_file:
        dump(user_data, output_file, indent = 4)
    logging.info("Data written.")
    
    logging.info("Exiting...")
    exit(0)
 

# if __name__ == "__main__":
#     logger_format = "[%(asctime)s] [%(levelname)s]: %(message)s"
#     logger_date_format = "%m/%d/%Y %I:%M:%S %p"
#     logger_file = logfile_setup()
#     logging.basicConfig(filename = logger_file, format = logger_format, datefmt = logger_date_format, level = logging.DEBUG)

#     main()
