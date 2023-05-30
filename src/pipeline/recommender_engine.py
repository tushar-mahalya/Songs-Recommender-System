from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from src.logger import logging


@dataclass
class RecommenderEngineConfig:
    prep_songs_data_path: str = 'artifacts/[Songs]_Preprocessed_Data.csv'
    prep_feats_data_path: str = 'artifacts/[Features]_Preprocessed_Data.csv'


class RecommenderEngine:

    def __init__(self):
        config = RecommenderEngineConfig()
        self._songs_data = pd.read_csv(config.prep_songs_data_path)
        self._features_data = pd.read_csv(config.prep_feats_data_path)
        logging.info('Preprocessed Songs & Features data read Successfully.')

    @staticmethod
    def getIndex(song_list: list, data_df: pd.DataFrame):
        index = data_df[data_df['Song-Artist'].isin(song_list)].index
        return index

    @staticmethod
    def removeIndexfromDF(song_idx: list, data_df: pd.DataFrame):
        new_df = data_df.drop(song_idx, axis=0)
        return new_df

    @staticmethod
    def songSummarizationVector(song_idx: list, data_df: pd.DataFrame):
        song_sum = data_df.iloc[song_idx].sum(axis=0)
        song_sum = song_sum.values.reshape(1, -1)
        return song_sum

    @staticmethod
    def getSimilarityDF(data_df: pd.DataFrame, summary_vector: np.ndarray):
        similarity_array = cosine_similarity(data_df.values, summary_vector)[:, 0]
        similarity_df = pd.DataFrame(similarity_array, columns=['similarity'])
        return similarity_df

    def Recommend_Songs(self, song_list_playlist: list) -> pd.DataFrame:
        song_list_playlist_idx = self.getIndex(song_list_playlist, self._songs_data)
        clean_feats_df = self.removeIndexfromDF(song_list_playlist_idx, self._features_data)
        playlist_summary_arr = self.songSummarizationVector(song_list_playlist_idx, self._features_data)
        similarity_df = self.getSimilarityDF(clean_feats_df, playlist_summary_arr)
        recommendations_idx = similarity_df.sort_values(by=['similarity'], ascending=False)[:100].index
        return self._songs_data.iloc[recommendations_idx]
