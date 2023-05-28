import sys
import pandas as pd
from dataclasses import dataclass

from src.components.preprocessing import combineSongArtist, removeDuplicates
from src.components.preprocessing import TFIDF_Features, OHE_Column, Standardize_Features
from src.components.sentiment import Sentiment_Features

from src.exception import CustomException
from src.logger import logging

@dataclass
class DataWranglingConfig:
    data_path: str = 'data/[Spotify]_Billboard_Hot100_Songs_1946-2022.csv'
    
class DataPreprocessing:
    def __init__(self):
        config = DataWranglingConfig()
        self._data = pd.read_csv(config.data_path)
        logging.info('Data read successfully from /data directory.')


    def data_preprocessing(self, data_df: pd.DataFrame):
        try:
            logging.info('Data Preprocessing started.')
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
            logging.info('Data Preprocessing completed.')
            return prep_df, final_df
        
        except Exception as e:
            raise CustomException(e,sys) 

    def get_preprocessed_data(self):
        try:
            songs_data, feats_data = self.data_preprocessing(self._data)
            songs_data.to_csv('artifacts/[Songs]_Preprocessed_Data.csv', index = False)
            feats_data.to_csv('artifacts/[Features]_Preprocessed_Data.csv', index = False)
            logging.info('Preprocessed Data and Features Data is stored in /artifacts directory.')
            return songs_data, feats_data
        except Exception as e:
            raise CustomException(e,sys)