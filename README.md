# FinalProject API

## Description
영화 커뮤니티 백앤드 API 백앤드 서버입니다. 

## Movie Data Crolling

> [The Movie DB API]() 에서 영화 데이터를 가져와 .json 파일을 생성했습니다.

- 요청

```python
import requests

ret = []
for page in range(1, 51):
  url = "https://api.themoviedb.org/3/movie/popular?api_key=API_KEY&language=en-US&page=" + str(page)
  res = requests.get(url).json()
  movies = res["results"]
  for movie in movies:
      inner = dict()
      # ... json(inner) 구성 ...
    ret.append(inner)
```

- 파일 생성

```python
# 위에서 만들어진 ret을 사용

import json

file = open("moviedata.json", "w+")
file.write(json.dumps(ret))
```

## LoadData
```commandline
$ python manage.py loaddata data/genredata.json
$ python manage.py loaddata data/moviedata.json
```

## Model
![KakaoTalk_Photo_2020-06-11-16-11-17](https://user-images.githubusercontent.com/53211781/84362975-03ffcb80-ac09-11ea-92cd-13c5ee787be9.png)

## API Guide
### 1. 전체 영화 조회하기 `GET` `/api/v1/community/movies/`
> id(영화 고유 personal key), genre, title, overview, poster_url, release_date
> 

### 2. 개별 영화 조회하기 `GET` `/api/v1/community/movies/<int:movie_pk>/`

### 3. 개별 아티클 조회하기 `GET` `/api/v1/community/articles/<int:article_pk>/`

### 4. 개별 아티클 생성하기 `POST` `/api/v1/community/articles/<int:movie_pk>/`

### 5. 댓글 작성하기 `POST` `/api/v1/community/articles/<int:article_pk>/comments/`

### 6. 로그인 회원정보 조회하기 `GET` `/api/v1/accounts/`

### 7. 개별 회원정보 조회하기 `GET` `/api/v1/accounts/<int:user_pk>/`