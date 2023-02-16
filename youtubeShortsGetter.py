import LikedShortsGetter
from elasticsearch import Elasticsearch

class youtubeShortsGetter:
    """Uses YouTube as source for shorts"""
    
    def __init__(self) -> None:
        auth_filepath = LikedShortsGetter.get_config_filepath()
        auth_info = LikedShortsGetter.load_auth_info(auth_filepath)
        user_data = LikedShortsGetter.get_liked_videos(auth_info)


    def getCategories(self) -> dict:
        """Returns a dictionary of the video categories, with an int as a key and string as values"""
        pass

    def getShortsOfCategory(self, int) -> dict:
        """Given an int, returns jsons of all videos in that category"""
        pass