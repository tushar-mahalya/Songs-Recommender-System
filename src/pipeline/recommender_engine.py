import os
import pandas as pd
import numpy as np
import sys
import json
from sklearn.metrics.pairwise import cosine_similarity

from src.components.preprocessing import combineSongArtist, removeDuplicates
from src.components.preprocessing import TFIDF_Features, OHE_Column, Standardize_Features
from src.components.sentiment import Sentiment_Features

from src.exception import CustomException
from src.logger import logging

from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    data_path: str = 'data/[Spotify]_Billboard_Hot100_Songs_1946-2022.csv'
    
    
class RecommenderEngine():
    
    def __init__(self):
        config = DataIngestionConfig()
        self.data = pd.read_csv(config.data_path)
        
        
    def data_preprocessing(self, data_df: pd.DataFrame):
        
        prep_df = combineSongArtist(data_df)
    
        prep_df = removeDuplicates(prep_df)

        genre_df = TFIDF_Features(prep_df)

        subject_df, polar_df = Sentiment_Features(prep_df, 'Song')

        key_ohe = OHE_Column(prep_df, 'Key', 'Key') * 0.5
        mode_ohe = OHE_Column(prep_df, 'Mode', 'Mode') * 0.5
        time_sig_ohe = OHE_Column(prep_df, 'Time Signature', 'Time Signature') * 0.5
        subject_ohe = OHE_Column(subject_df, 'subjectivity', 'Subjectivity') * 0.5
        polar_ohe = OHE_Column(polar_df, 'polarity', 'Polarity') * 0.5

        num_feats = ['Popularity', 'Acousticness', 'Danceability', 'Energy', 'Instrumentalness',
                     'Liveness', 'Loudness', 'Speechiness','Tempo', 'Valence']
        scaled_feats = Standardize_Features(prep_df, num_feats)

        final_df = pd.concat([genre_df, subject_ohe, polar_ohe, key_ohe, mode_ohe,
                              time_sig_ohe, scaled_feats], axis = 1)
        
        return final_df
    
    
    def getIndex(self, song_list: list, data_df: pd.DataFrame):
        index = data_df[data_df['Song-Artist'].isin(song_list)].index
        return index
    
    
    def removeIndexfromDF(self, song_idx: list, data_df: pd.DataFrame):
        new_df = data_df.drop(song_idx, axis = 0)
        return new_df
    
    
    def songSummarizationVector(self, song_idx: list, data_df: pd.DataFrame):
        song_sum = data_df.iloc[song_idx].sum(axis = 0)
        song_sum = song_sum.values.reshape(1, -1)
        return song_sum
    
    
    def getSimilarityDF(self, data_df: pd.DataFrame, summary_vector: np.ndarray):
        similarity_array = cosine_similarity(data_df.values, summary_vector)[:,0]
        similarity_df = pd.DataFrame(similarity_array, columns = ['similarity'])
        return similarity_df
    
    
        
    
if __name__ == '__main__':
    config = DataIngestionConfig()
    data = pd.read_csv(config.data_path)
    print('Data Read')