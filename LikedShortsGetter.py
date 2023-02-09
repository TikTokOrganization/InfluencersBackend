import requests, logging
from json import load, dump
from os import path, mkdir, listdir
from sys import exit


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


def get_liked_videos(auth_info: str) -> dict:
    """Make a request to Youtube API to get a user's liked videos."""

    token_url = "https://accounts.google.com/o/oauth2/token"
    api_url = "https://youtube.googleapis.com/youtube/v3/videos"
    search_params = {
        "myRating": "like",
        "key": "AIzaSyBEDqAaPKfAOqKvw8EjTLlI7A4JE1cmR9M",
        "part": "snippet,contentDetails,statistics",
    }

    #Use refresh token (unchanging) to get a new access token (need new one every time) also using client id and client secret
    token_response = requests.post(token_url, data = auth_info)
    if token_response.status_code != 200:
        logging.error(f"Token request failed, server returned {token_response.status_code}")
        exit(0)
    token = token_response["access_token"]

    #Make the request to the api using api key and token
    search_headers = {"Authorization": "Bearer " + token, "Accept": "application/json"}
    search_response = requests.get(api_url, headers = search_headers, params = search_params)
    if search_response.status_code != 200:
        logging.error(f"Search request failed, server returned {search_response.status_code}")
        exit(0)

    return dict(search_response.json)


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
 

if __name__ == "__main__":
    logger_format = "[%(asctime)s] [%(levelname)s]: %(message)s"
    logger_date_format = "%m/%d/%Y %I:%M:%S %p"
    logger_file = logfile_setup()
    logging.basicConfig(filename = logger_file, format = logger_format, datefmt = logger_date_format, level = logging.DEBUG)

    main()
