from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
import sqlite3
import os

class Movie(BaseModel):
    title: str
    year: str
    actors: str

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ŚCIEŻKA DO FRONTENDU W DOCKERZE
BUILD_DIR = "/var/app/ui/build"

# Serwowanie statycznych plików Reacta
app.mount("/static", StaticFiles(directory=os.path.join(BUILD_DIR, "static")), name="static")

@app.get("/")
def serve_react_app():
    return FileResponse(os.path.join(BUILD_DIR, "index.html"))

# --- ENDPOINTY FILMÓW ---

@app.get('/movies')
def get_movies():
    db = sqlite3.connect('movies.db')
    cursor = db.cursor()
    movies = cursor.execute('SELECT * FROM movies')

    output = []
    for movie in movies:
        output.append({
            'id': movie[0],
            'title': movie[1],
            'year': movie[2],
            'actors': movie[3]
        })
    return output

@app.get('/movies/{movie_id}')
def get_single_movie(movie_id: int):
    db = sqlite3.connect('movies.db')
    cursor = db.cursor()
    movie = cursor.execute("SELECT * FROM movies WHERE id=?", (movie_id,)).fetchone()
    if movie is None:
        return {'message': "Movie not found"}
    return {'title': movie[1], 'year': movie[2], 'actors': movie[3]}

@app.post("/movies")
def add_movie(movie: Movie):
    db = sqlite3.connect('movies.db')
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO movies (title, year, actors) VALUES (?, ?, ?)",
        (movie.title, movie.year, movie.actors)
    )
    db.commit()
    return {"message": f"Movie with id = {cursor.lastrowid} added successfully"}

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, params: dict[str, Any]):
    db = sqlite3.connect('movies.db')
    cursor = db.cursor()
    cursor.execute(
        "UPDATE movies SET title = ?, year = ?, actors = ? WHERE id = ?",
        (params['title'], params['year'], params['actors'], movie_id)
    )
    db.commit()
    if cursor.rowcount == 0:
        return {"message": f"Movie with id = {movie_id} not found"}
    return {"message": f"Movie with id = {movie_id} updated successfully"}

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    db = sqlite3.connect('movies.db')
    cursor = db.cursor()
    cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    db.commit()
    if cursor.rowcount == 0:
        return {"message": f"Movie with id = {movie_id} not found"}
    return {"message": f"Movie with id = {movie_id} deleted successfully"}

@app.delete("/movies")
def delete_movies():
    db = sqlite3.connect('movies.db')
    cursor = db.cursor()
    cursor.execute("DELETE FROM movies")
    db.commit()
    return {"message": f"Deleted {cursor.rowcount} movies"}
