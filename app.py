from fastapi import FastAPI, HTTPException
from src.recommender import get_movie_recommendation

app = FastAPI(title="Movie Recommender API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie Recommender API. Use /recommend/{movie_name} to get started."}

@app.get("/recommend/{movie_name}")
def recommend(movie_name: str):
    # Call your existing logic
    result = get_movie_recommendation(movie_name)

    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")

    return {"result": result}

# To run this, use the command: uvicorn app:app --reload