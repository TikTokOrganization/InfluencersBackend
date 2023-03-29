import requests


class YTShortsRetriever:
    SHORT_VALIDATOR_URI = "https://yt.lemnoslife.com/videos"
    SHORT_SEARCH_URI = "https://youtube.googleapis.com/youtube/v3/videos"
    CATEGORY_ID_CODES = {
        "1": "Film & Animation",
        "2": "Autos & Vehicles",
        "10": "Music",
        "15": "Pets & Animals",
        "17": "Sports",
        "18": "Short Movies",
        "19": "Travel & Events",
        "20": "Gaming",
        "21": "Videoblogging",
        "22": "People & Blogs",
        "23": "Comedy",
        "24": "Entertainment",
        "25": "News & Politics",
        "26": "Howto & Style",
        "27": "Education",
        "28": "Science & Technology",
        "29": "Nonprofits & Activism",
        "30": "Movies",
        "31": "Anime/Animation",
        "32": "Action/Adventure",
        "33": "Classics",
        "34": "Comedy",
        "35": "Documentary",
        "36": "Drama",
        "37": "Family",
        "38": "Foreign",
        "39": "Horror",
        "40": "Sci-Fi/Fantasy",
        "41": "Thriller",
        "42": "Shorts",
        "43": "Shows",
        "44": "Trailers"
    }

    def __init__(self, access_token):
        self.__access_token = access_token
        self.cache = None
    
    def get_access_token(self):
        return self.__access_token

    def set_access_token(self, access_token):
        self.__access_token = access_token

    def get_categoryID_codes(self):
        return self.CATEGORY_ID_CODES

    def make_request(self, uri, request_params):
        response = False

        try:
            response = requests.get(uri, params = request_params)
        except Exception as e:
            print(f"Error: {e}")
            return response
        
        if response.status_code != 200:
            print(f"Request failed, status code {response.status_code} recieved.")
            response = False

        return response

    def get_liked_videos(self):
        search_params = {
            "access_token": self.__access_token,
            "part": "snippet",
            "myRating": "like"
        }

        liked_videos = []
        repeat_request = True
        while repeat_request:
            search_response = self.make_request(self.SHORT_SEARCH_URI, search_params)
            if not search_response:
                liked_videos.insert(0, -1)
                repeat_request = False
            else:
                response_data = search_response.json()
                liked_videos.extend(response_data["items"])

                if "nextPageToken" in response_data.keys():
                    search_params["pageToken"] = response_data["nextPageToken"]
                else:
                    repeat_request = False
        
        if liked_videos[0] == -1:
            #No requests were able to complete if the length of liked_videos is also 1
            liked_videos.pop(0)
        
        return liked_videos

    def get_liked_shorts(self, liked_videos):
        liked_shorts = {"items": [], "validator_failure": 0}
        for video in liked_videos:
            validator_params = {
                "part": "short",
                "id": video["id"]
            }

            validator_response = self.make_request(self.SHORT_VALIDATOR_URI, validator_params)
            if not validator_params:
                liked_shorts["validator_failure"] += 1
                continue    #TODO: Add better error handling
            
            response_data = validator_response.json()
            if response_data["items"][0]["short"]["available"]:
                liked_shorts["items"].append(video)

        if liked_shorts["validator_failure"] == len(liked_videos):
            #All validation requests failed
            liked_shorts = False
        else:
            del liked_shorts["validator_failure"]
        
        return liked_shorts

    def prepare_shorts(self, liked_shorts):
        prepared_data = False

        if not liked_shorts:
            return prepared_data
        
        prepared_data = {"shorts": {}}
        liked_shorts = liked_shorts["items"]
        for short in liked_shorts:
            category = short["snippet"]["categoryId"]
            short_data = {
                "id": short["id"],
                "category": category,
                "thumbnailURL": short["snippet"]["thumbnails"]["default"]["url"]
            }

            if category in prepared_data["shorts"].keys():
                prepared_data["shorts"][category].append(short_data)
            else:
                prepared_data["shorts"][category] = [short_data]
        self.cache = prepared_data

        prepared_data["category_codes"] = self.CATEGORY_ID_CODES
        prepared_data["total"] = len(liked_shorts)

        return prepared_data

    def get_content(self, refresh):
        if refresh or not self.cache:
            liked_videos = self.get_liked_videos()
            liked_shorts = self.get_liked_shorts(liked_videos)
            pruned_liked_shorts = self.prepare_shorts(liked_shorts)
        else:
            pruned_liked_shorts = self.cache

        return pruned_liked_shorts