from fastapi import FastAPI, HTTPException
from src.data_preprocessing import get_preprocessed_data
from src.recommender import get_movie_recommendation
import pandas as pd

app = FastAPI(title="Movie Recommender API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie Recommender API. Use /recommend/{movie_name} to get started."}

@app.get("/recommend/{movie_name}")
def recommend(movie_name: str):
    # Call your existing logic
    result = get_movie_recommendation(movie_name)
        
    return {"result": result}

# To run this, use the command: uvicorn app:app --reload