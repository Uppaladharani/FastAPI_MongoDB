import requests

url = "http://localhost:8000/movies/"

movies = [
    {"title": "murari", "director": "Krishna Vamsi", "year": 2001},
]

for movie in movies:
    response = requests.post(url, json=movie)
    if response.status_code == 200:
        print(f"Added movie: {response.json()}")
    else:
        print(f"Failed to add movie: {response.status_code}, {response.text}")
