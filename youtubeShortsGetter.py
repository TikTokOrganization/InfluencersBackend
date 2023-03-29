import LikedShortsGetter
import requests, json, os
from elasticsearch import Elasticsearch 
import time

#for finding similar words
import gensim
import nltk
from nltk.data import find

class youtubeShortsGetter:
    """Uses YouTube as source for shorts"""
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

    def __init__(self) -> None:
        pass


    def getCategories(self) -> dict:
        """Returns a dictionary of the video categories, with an int as a key and string as values"""
        return youtubeShortsGetter.category_id

    def addCategory(self, catNum, catName) -> None:
        """ Update the category dict when a user creates a new category """
        youtubeShortsGetter.category_id[str(catNum)] = str(catName)
        return youtubeShortsGetter.category_id 
        
    def removeCategory(self, catNum) -> None:
        """ Remove a category from category dict """
        remove = youtubeShortsGetter.category_id.pop(str(catNum))
        return youtubeShortsGetter.category_id

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
                        "my_stemmer", 
                        "stop"
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

        time.sleep(0.5)
        es.indices.create(index='myindex', body = analyzer_body)

        # Send the data into es
        Bbody=json.loads(docket_content)

        #loads each youtube short into the index
        for video in Bbody["items"]:
            es.index(index='myindex', ignore=400, body = video)
    
        return es

    def getShortsOfCategory(self, es):
        """Returns dictionary where key = category & value = liked videos"""
        categories = youtubeShortsGetter.category_id

        likedCategories = {}

        for c in categories.keys():
            val = youtubeShortsGetter.category_id.get(c)
            my_body = {
                "query": {
                    "term" : {
                        "snippet.categoryId.keyword": c,
                    }
                },
                "size":1000
            }

            #time.sleep(0.5)
            r = es.search(index='myindex', body = my_body)

            if(len(r["hits"]["hits"]) != 0):
                likedCategories[str(val)] = r["hits"]["hits"]

        return likedCategories

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

        r = es.search(index='myindex', body = my_body)

        return r["hits"]["hits"]
        

    def getSimilarWords(self, word, es):
        """ Returns KNN for a inputted word """
        
        #get pretrained model (trained on Google News Dataset)
        word2vec_sample = str(find('models/word2vec_sample/pruned.word2vec.txt'))
        model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_sample, binary=False)

        try:
            #returns top K related words
            values = model.most_similar(positive=[word], topn = 20)

            ans = []
            for x in values:
                ans.append(x[0])

        except KeyError:
            ans = word
        
        my_body = {
            "query": {
                "more_like_this" : {
                    "fields": ['snippet.title', 'snippet.description', 'snippet.channelTitle', 'snippet.tags'],
                    "like" : ans,
                    "min_term_freq" : 1,
                    "min_doc_freq" : 1,
                    "max_doc_freq" : 1000

                }
            }, 
            "size":1000
        } 


        r = es.search(index='myindex', body = my_body)

        return r["hits"]["hits"]

