from src.ContentRetriever.YTShortsRetriever import YTShortsRetriever
from src.ContentRetriever.StaticFileRetriever import StaticFileRetriever


class MediaRetriever:
    def __init__(self, failsafe_source):
        self.ytShortsRetriever = YTShortsRetriever(None)
        self.staticFileRetriever = StaticFileRetriever(failsafe_source)
    
    def update_source(self, access_token):
        self.ytShortsRetriever.set_access_token(access_token)
    
    def get_content(self, refresh, failsafe = False):
        if failsafe or not self.ytShortsRetriever.get_access_token():
            content = self.staticFileRetriever.get_content()
        else:
            content = self.ytShortsRetriever.get_content(refresh)
            if not content:
                content = self.staticFileRetriever.get_content()
        
        return content