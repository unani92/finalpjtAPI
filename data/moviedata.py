from pprint import pprint
import requests, json

ret = []

for page in range(1, 6):

    url = "https://api.themoviedb.org/3/movie/popular?api_key=44084423a3ad71eb2acee3298e9a25e8&language=en-US&page=" + str(page)
    res = requests.get(url).json()

    movies = res["results"]


    for movie in movies:
        inner = dict()
        inner["model"] = "community.movie"
        inner["pk"] = movie["id"]

        fields = dict()

        fields["title"] = movie["original_title"]
        fields["overview"] = movie["overview"]
        fields["poster_path"] = movie["poster_path"]
        fields["release_date"] = movie["release_date"]
        fields["popularity"] = movie["popularity"]
        fields["vote_count"] = movie["vote_count"]
        fields["vote_average"] = movie["vote_average"]
        fields["adult"] = movie["adult"]
        fields["genres"] = movie["genre_ids"]

        inner["fields"] = fields

        ret.append(inner)

file = open("moviedata.json", "w+")
file.write(json.dumps(ret))