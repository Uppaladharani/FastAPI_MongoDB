from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from typing import List

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["movie_db"]
collection = db["movies"]

class Movie(BaseModel):
    title: str
    director: str
    year: int

def movie_helper(movie) -> dict:
    return {
        "id": str(movie["_id"]),
        "title": movie["title"],
        "director": movie["director"],
        "year": movie["year"]
    }

@app.post("/movies/", response_model=Movie)
async def create_movie(movie: Movie):
    movie_dict = movie.dict()
    result = collection.insert_one(movie_dict)
    movie_dict["_id"] = result.inserted_id
    return movie_helper(movie_dict)

@app.get("/movies/", response_model=List[Movie])
async def get_movies():
    movies = []
    for movie in collection.find():
        movies.append(movie_helper(movie))
    return movies

@app.get("/movies/{movie_id}", response_model=Movie)
async def get_movie(movie_id: str):
    movie = collection.find_one({"_id": ObjectId(movie_id)})
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie_helper(movie)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
