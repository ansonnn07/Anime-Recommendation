import joblib
import pandas as pd
import numpy as np
import os
from .config import Config
from injector import inject

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Activation, BatchNormalization, Embedding, Dot, Dense, Flatten

N_USERS = 145311
N_ANIMES = 17562
USER_EMB_SIZE = 128
ANIME_EMB_SIZE = 128
EMBEDDING_SIZES = (USER_EMB_SIZE, ANIME_EMB_SIZE)
ANIME_EMB_LAYER_NAME = 'anime_embedding'

ENCODERS_DICT = joblib.load(os.path.join(
    Config.ASSETS_PATH, 'encoder_dicts.joblib'))


class RecommenderModel(keras.models.Model):
    def __init__(self, n_users, n_animes, embedding_sizes, activation='relu', **kwargs):
        super().__init__(**kwargs)
        self.user_embedding = Embedding(
            name='user_embedding',
            input_dim=n_users,
            output_dim=embedding_sizes[0],
        )
        self.anime_embedding = Embedding(
            name=ANIME_EMB_LAYER_NAME,
            input_dim=n_animes,
            output_dim=embedding_sizes[1],
        )
        self.dot_layer = Dot(name='dot_product', normalize=True, axes=1)
        self.layers_ = [
            Flatten(),
            Dense(128, activation=activation, use_bias=False,
                  kernel_initializer='he_normal'),
            BatchNormalization(),
            Dense(64, activation=activation, use_bias=False,
                  kernel_initializer='he_normal'),
            BatchNormalization(),
            Dense(1, use_bias=False, kernel_initializer='he_normal'),
            BatchNormalization(),
            Activation('sigmoid'),
        ]

    def call(self, inputs):
        user_vector = self.user_embedding(inputs[:, 0])
        anime_vector = self.anime_embedding(inputs[:, 1])
        x = self.dot_layer([user_vector, anime_vector])
        for layer in self.layers_:
            x = layer(x)
        return x


class Model:
    def __init__(self):
        # Actually can just serialize the anime_weights attribute enough,
        #  as it is the only one needed for making recommendations in this case.
        #  But I still left everything as it is, because most of the time it is required
        #  to deploy models like this.
        self.anime_id_to_idx = ENCODERS_DICT['anime_id_to_idx']
        self.anime_idx_to_id = ENCODERS_DICT['anime_idx_to_id']
        self.user_id_to_idx = ENCODERS_DICT['user_id_to_idx']
        self.n_users, self.n_animes = len(
            self.user_id_to_idx), len(self.anime_id_to_idx)
        self.emb_sizes = EMBEDDING_SIZES

        self.model = self.load_model()
        self.anime_weights = self.extract_weights(ANIME_EMB_LAYER_NAME)

        self.df = pd.read_csv(os.path.join(
            Config.DATA_PATH, 'full_anime_info.csv'))

        print(f"\n[INFO] Model instance is initialized!\n")

    def load_model(self):
        model = RecommenderModel(
            self.n_users, self.n_animes, self.emb_sizes)
        model.compile(loss='binary_crossentropy', metrics=[
            'mae', 'mse'], optimizer='adam')
        print('\n[INFO] Calling model to load layers...\n')
        _ = model(tf.ones((1, 2)))
        model.load_weights(os.path.join(Config.ASSETS_PATH, 'weights.h5'))
        print('\n[INFO] Loaded weights.\n')
        return model

    def extract_weights(self, name):
        weight_layer = self.model.get_layer(name)
        weights = weight_layer.get_weights()[0]
        # Dot layer was using normalize=True to compute cosine similarity
        weights = tf.math.l2_normalize(weights, axis=1).numpy()
        return weights


class InitializedModel:
    @inject
    def __init__(self, model: Model):
        self.anime_id_to_idx = model.anime_id_to_idx
        self.anime_idx_to_id = model.anime_idx_to_id
        self.anime_weights = model.anime_weights
        self.df = model.df

    def get_recommendation(self, anime_query, k=30):
        """Generate recommendations based on given Anime ID.

        Args:
            anime_query (int): Anime ID
            k (int, optional): Number of animes to recommend. Defaults to 30.

        Raises:
            Exception: Anime ID not found in MyAnimelist database.

        Returns:
            anime_query_row (pd.DataFrame) : Anime record of the query requested by user.
            rec_anime_df (pd.DataFrame): Pandas DataFrame consisting of list of 
                recommended Animes.
        """
        anime_query_rows = self.df[self.df.MAL_ID == int(anime_query)]
        if len(anime_query_rows) == 0:
            raise Exception(f'Anime not found for {anime_query}')
        anime_query_row = anime_query_rows.iloc[[0]]
        anime_id = anime_query_row.MAL_ID.values[0]
        anime_name = anime_query_row.Name.values[0]
        anime_idx = self.anime_id_to_idx.get(anime_id)

        weights = self.anime_weights
        distances = np.dot(weights, weights[anime_idx])

        sorted_dists_ind = np.argsort(distances)[::-1]

        print(f'Recommending animes for {anime_name}')

        anime_list = []
        # [1:] to skip the first row for anime_query
        for idx in sorted_dists_ind[1:]:
            # similarity = distances[idx]
            anime_id = self.anime_idx_to_id.get(idx)
            anime_row = self.df[self.df.MAL_ID == anime_id]
            new_synopsis = anime_row.new_synopsis.values[0]
            anime_name = anime_row.Name.values[0]
            score = anime_row.Score.values[0]
            genre = anime_row.Genres.values[0]
            img_url = anime_row.img_url.values[0]

            anime_list.append({"MAL_ID": anime_id, "Name": anime_name,
                               "img_url": img_url, "Score": score,
                               "new_synopsis": new_synopsis, "Genres": genre
                               })
            if len(anime_list) == k:
                # enough number of recommendations
                break
        rec_df = pd.DataFrame(anime_list)
        return anime_query_row, rec_df
