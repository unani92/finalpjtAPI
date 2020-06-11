from pprint import pprint
import requests, json

ret = []

url = "https://api.themoviedb.org/3/genre/movie/list?language=en-US&api_key=44084423a3ad71eb2acee3298e9a25e8"
res = requests.get(url).json()
genres = res['genres']

for genre in genres:
    inner = dict()
    inner["model"] = "community.genre"
    inner["pk"] = genre["id"]

    fields = dict()
    fields["name"] = genre["name"]
    inner["fields"] = fields

    ret.append(inner)

file = open("genredata.json", "w+")
file.write(json.dumps(ret))