import pandas as pd
from sklearn.neighbors import NearestNeighbors
from src.data_preprocessing import get_preprocessed_data

# ----------------------------
# Load data ONCE (important)
# ----------------------------
final_dataset, csr_data, movies = get_preprocessed_data()

# ----------------------------
# Train KNN model ONCE
# ----------------------------
knn = NearestNeighbors(
    metric="cosine",
    algorithm="brute",
    n_neighbors=20,
    n_jobs=-1
)
knn.fit(csr_data)


# ----------------------------
# Recommendation function
# ----------------------------
def get_movie_recommendation(movie_name: str, n_recommendations: int = 10):
    # Find movie by title (partial match)
    movie_list = movies[movies["title"].str.contains(movie_name, case=False, na=False)]

    if movie_list.empty:
        return {"error": "No movies found. Please check your input."}

    # Get movieId
    movie_id = movie_list.iloc[0]["movieId"]

    # Check if movie exists in filtered dataset
    if movie_id not in final_dataset["movieId"].values:
        return {"error": "Movie exists but not enough ratings to generate recommendations."}

    # Get index in CSR matrix
    movie_idx = final_dataset[final_dataset["movieId"] == movie_id].index[0]

    # Find nearest neighbors
    distances, indices = knn.kneighbors(
        csr_data[movie_idx],
        n_neighbors=n_recommendations + 1
    )

    # Remove the movie itself and sort by distance
    recommendations = sorted(
        zip(indices.squeeze().tolist(), distances.squeeze().tolist()),
        key=lambda x: x[1]
    )[1:]

    # Build response
    results = []
    for idx, distance in recommendations:
        rec_movie_id = final_dataset.iloc[idx]["movieId"]
        title = movies[movies["movieId"] == rec_movie_id]["title"].values[0]

        results.append({
            "title": title,
            "similarity_score": round(1 - distance, 3)
        })

    return results