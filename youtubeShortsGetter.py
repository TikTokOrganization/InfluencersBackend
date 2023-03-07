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


    def initializeElasticIndex(self) -> None:
        #connects to elasticsearch
        es = Elasticsearch('http://localhost:9200')

        #deletes index if it exists and loads json file with all of the liked videos
        if es.indices.exists(index="myindex"):
            es.indices.delete(index='myindex', ignore=[400, 404])

        f = open("finalOutput.json", encoding = "utf-8")
        docket_content = f.read()

        #changes index settings so that singular/plural words can be parsed together
        analyzer_body = {
            "settings": {
                "analysis": {
                "analyzer": {
                    "my_analyzer": {
                    "type": "custom",
                    "filter": [
                        "lowercase",
                        "my_stemmer"
                    ],
                    "tokenizer": "whitespace"
                    }
                },
                "filter": {
                    "my_stemmer": {
                    "type": "stemmer",
                    "name": "english"
                    }
                }
            }
            },
            "mappings": {
                "properties": {
                    "snippet.title": {
                    "type": "text",
                    "analyzer": "my_analyzer",
                        "fields": {
                            "keyword": {
                            "type": "keyword"
                            }
                        }
                    },
                    "snippet.description": {
                    "type": "text",
                    "analyzer": "my_analyzer",
                        "fields": {
                            "keyword": {
                            "type": "keyword"
                            }
                        }
                    },
                    "snippet.channelTitle": {
                    "type": "text",
                    "analyzer": "my_analyzer",
                        "fields": {
                            "keyword": {
                            "type": "keyword"
                            }
                        }
                    },
                    "snippet.tags": {
                        "type": "text",
                        "analyzer": "my_analyzer",
                        "fields": {
                            "keyword": {
                            "type": "keyword"
                            }
                        }
                    }
                }
            }
        }

        time.sleep(2)
        es.indices.create(index='myindex', body = analyzer_body)

        # Send the data into es
        Bbody=json.loads(docket_content)

        #loads each youtube short into the index
        for video in Bbody["items"]:
            es.index(index='myindex', ignore=400, body = video)
    
        return es

    def getShortsOfCategory(self, catNum: int, es) -> list:
        """Returns a list of shorts based on category number input (int) """

        my_body = {
            "query": {
                "term" : {
                    "snippet.categoryId.keyword": str(catNum),
                }
            },
            "size":1000
        }

        time.sleep(2)
        r = es.search(index='myindex', body = my_body)

        return r["hits"]["hits"]

    def getMoreLikeThis(self, tagName, es)-> list:
        """Returns all videos that contain tagName (string) - may be useful for user-made categories and search functionality """

        my_body = {
            "query": {
                "more_like_this" : {
                    "fields": ['snippet.title', 'snippet.description', 'snippet.channelTitle', 'snippet.tags'],
                    "like" : tagName,
                    "min_term_freq" : 1,
                    "min_doc_freq" : 1,
                    "max_doc_freq" : 1000

                }
            }, 
            "size":1000
        } 

        time.sleep(2)
        r = es.search(index='myindex', body = my_body)

        return r["hits"]["hits"]
        














