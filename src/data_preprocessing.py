import pandas as pd
from scipy.sparse import csr_matrix

def get_preprocessed_data():
    # 1. Load Data
    # Note: We use 'data/' because app.py runs from the root
    movies = pd.read_csv("data/movies.csv")
    rating = pd.read_csv("data/ratings.csv")

    # 2. Pivot and Fill
    final_dataset = rating.pivot(index="movieId", columns="userId", values="rating")
    final_dataset.fillna(0, inplace=True)

    # 3. Aggregate Votes
    no_user_voted = rating.groupby("movieId")["rating"].agg("count")
    no_movies_voted = rating.groupby("userId")["rating"].agg("count")

    # 4. Filter
    final_dataset = final_dataset.loc[no_user_voted[no_user_voted > 10].index, 
                                      no_movies_voted[no_movies_voted > 50].index]

    # 5. Prepare CSR and Reset Index
    csr_data = csr_matrix(final_dataset.values)
    final_dataset.reset_index(inplace=True)
    
    return final_dataset, csr_data, movies