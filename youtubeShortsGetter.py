import LikedShortsGetter
import requests, json, jsons, os
from elasticsearch import Elasticsearch 
import time

class youtubeShortsGetter:
    """Uses YouTube as source for shorts"""
    
    def __init__(self) -> None:
        auth_filepath = LikedShortsGetter.get_config_filepath()
        auth_info = LikedShortsGetter.load_auth_info(auth_filepath)
        user_data = LikedShortsGetter.get_liked_videos(auth_info)


    def getCategories(self) -> dict:
        """Returns a dictionary of the video categories, with an int as a key and string as values"""
        category_id = {
            "1": "Film & Animation",
            "2": "Autos & Vehicles",
            "10": "Music",
            "15": "Pets & Animals",
            "17": "Sports",
            "18": "Short Movies",
            "19": "Travel & Events",
            "20": "Gaming",
            "21": "Videoblogging",
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

        return category_id

    def getShortsOfCategory(self, int) -> list:
        """Returns a list of jsons based on category number input (int) """
        es = Elasticsearch('http://localhost:9200')
        if es.indices.exists(index="myindex"):
            es.indices.delete(index='myindex', ignore=[400, 404])

        f = open("finalOutput.json", encoding = "utf-8")
        docket_content = f.read()

        es.indices.create(index='myindex')

        # Send the data into es
        Bbody=json.loads(docket_content)

        for video in Bbody["items"]:
            es.index(index='myindex', ignore=400, body = video)

        my_body = {
            "query": {
                "match" : {
                    "snippet.categoryId.keyword": str(catNum)
                }
            }
        }
        time.sleep(2)
        r = es.search(index='myindex', body = my_body)

        return r["hits"]["hits"]















