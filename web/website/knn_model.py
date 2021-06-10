from collections import defaultdict
import joblib
import pandas as pd
import os
from .config import Config
from . import cache


def get_anime_rows(df, anime_name, exact_name=False, types=None):
    df = df.copy()
    if exact_name:
        # get exact name
        df = df[df.Name == anime_name]
    else:
        df = df[df.Name.str.contains(anime_name, case=False, regex=False) |
                df['English name'].str.contains(anime_name, case=False, regex=False)]

    if types:
        try:
            types = set([types]) if isinstance(types, str) else set(types)
            df = df[df.Type.isin(types)]
        except:
            raise Exception('Anime type not valid!')
    return df


@cache.cached(timeout=30, key_prefix='model_objs')
def load_model_objs():
    anime_encoders = joblib.load(os.path.join(
        Config.ASSETS_PATH, 'kNN_anime_encoders'))
    cf_df_values = joblib.load(os.path.join(
        Config.ASSETS_PATH, 'cf_df_values.joblib'))
    model = joblib.load(os.path.join(Config.ASSETS_PATH, 'kNN_model.joblib'))

    return anime_encoders, cf_df_values, model


def get_recommendation(anime_query, k=10, exact_name=False, types=None):
    """Generate recommendations based on given Anime ID or Anime name.

    Args:
        anime_query (int | str): Anime ID or Anime name
        k (int, optional): Number of animes to recommend. Defaults to 10.
        exact_name (bool, optional): Whether to search for anime name of 
            exact match, case sensitive. Defaults to False.
        types (str | list | tuple, optional): Types of anime,
            generally 'TV' type for Anime series. Defaults to None.

    Raises:
        Exception: Invalid type of query given.
        Exception: Anime ID not found in MyAnimelist database.

    Returns:
        anime_row (pd.DataFrame) : Anime record of the query requested by user.
        rec_anime_df (pd.DataFrame): Pandas DataFrame consisting of list of 
            recommended Animes.
    """
    anime_encoders, cf_df_values, model = load_model_objs()
    anime_id_to_idx = anime_encoders['anime_id_to_idx']
    anime_idx_to_id = anime_encoders['anime_idx_to_id']

    anime_df = pd.read_csv(os.path.join(
        Config.DATA_PATH, 'full_anime_info.csv'))

    if isinstance(anime_query, int):
        anime_id = anime_query
    elif isinstance(anime_query, str):
        anime_id = get_anime_rows(
            anime_df, anime_query, exact_name, types).iloc[0, 0]
    else:
        raise Exception(
            "Invalid type of query, must be either anime ID or name!")

    try:
        anime_idx = anime_id_to_idx.get(anime_id)
        # anime_cf_values = cf_df.loc[anime_id, :].values.reshape(1, -1)
        anime_cf_values = cf_df_values[anime_idx].reshape(1, -1)
    except:
        raise Exception("Anime ID not found in MyAnimelist!")
    distances, indices = model.kneighbors(anime_cf_values, n_neighbors=k + 1)
    distances, indices = distances.flatten(), indices.flatten()
    # rec_anime_df = pd.DataFrame(columns=['Anime', 'Distance'])
    rec_anime_dict = defaultdict(list)

    for i, (distance, idx) in enumerate(zip(distances, indices)):
        anime_id = anime_idx_to_id.get(idx)
        # anime_id = cf_df.iloc[idx].name
        if i == 0:
            anime_row = anime_df.loc[anime_df.MAL_ID == anime_id].copy()
            anime_name = anime_row.Name.values[0]
            print(f"Recommending for anime: {anime_name}\n")
        else:
            # print(f"{i}: {anime} \t Distance: {distance}")
            # rec_anime_df = rec_anime_df.append({'Anime': anime, 'Distance': distance}, ignore_index=True)
            rec_anime_dict['anime_id'].append(anime_id)
            rec_anime_dict['distance'].append(distance)

    rec_anime_df = anime_df.copy()
    rec_anime_df = rec_anime_df[rec_anime_df.MAL_ID.isin(
        rec_anime_dict['anime_id'])]
    # rec_anime_df['Distance'] = rec_anime_dict['distance']
    rec_anime_df.insert(3, 'Distance', rec_anime_dict['distance'])

    return anime_row, rec_anime_df
