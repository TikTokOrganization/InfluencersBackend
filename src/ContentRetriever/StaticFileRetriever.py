from json import load


class StaticFileRetriever:
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
    
    def __init__(self, source):
        self.source = source
    
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

        prepared_data["category_codes"] = self.CATEGORY_ID_CODES
        prepared_data["total"] = len(liked_shorts)

        return prepared_data

    def get_content(self):
        content = False

        try:
            with open(self.source, "r") as input_file:
                content = load(input_file)
        except IOError:
            print(f"Error accessing file.")
        except Exception as e:
            print(f"Error: {e}")

        return self.prepare_shorts(content)