from fastapi.testclient import TestClient
from unittest.mock import patch
from app import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint returns a welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

@patch("app.get_movie_recommendation")
def test_recommend_movie_found(mock_get_rec):
    """Test that a valid movie returns recommendations."""
    # Mock the recommender to return a list of movies
    mock_get_rec.return_value = ["Toy Story 2", "Finding Nemo"]
    
    response = client.get("/recommend/Toy Story")
    
    assert response.status_code == 200
    assert response.json() == {"result": ["Toy Story 2", "Finding Nemo"]}
    mock_get_rec.assert_called_once_with("Toy Story")

@patch("app.get_movie_recommendation")
def test_recommend_movie_not_found(mock_get_rec):
    """Test that a non-existent movie returns a 404 error."""
    # Mock the recommender to return an empty list (or None)
    mock_get_rec.return_value = []
    
    response = client.get("/recommend/Unknown Movie")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Movie not found"}