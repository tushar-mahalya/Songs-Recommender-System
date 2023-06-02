import os
import sys
import json
import configparser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from src.exception import CustomException
from src.logger import logging

from dataclasses import dataclass

from src.components.data_downloader import Billboards_Hot100_Chart, addURIColumn
from src.components.data_downloader import Spotify_Features

@dataclass
class DataIngestionConfig:
    cred_path: str = 'credentials.ini'
    spotify_data_path: str = 'data/[Spotify]_Billboard_Hot100_Songs_1946-2022.csv'
    wikipedia_data_path: str = 'data/[Wikipedia]_Billboard_Hot100_Songs_1946-2022.csv'
    
class DataIngestion:

    def __init__(self):
        config = DataIngestionConfig()
        parser = configparser.ConfigParser()
        parser.read(config.cred_path)
        
        self.spotify_client_id = parser.get('Spotify', 'client_id')
		self.spotify_client_secret = parser.get('Spotify', 'client_secret')
        
    @staticmethod
    def getSpotifyInstance(self):
        try:
            client_credentials_manager = SpotifyClientCredentials(client_id=self.spotify_client_id,
                                                                  client_secret=self.spotify_client_secret)
            sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
            logging.info('Connected to Spotify API.\nInstance created !')
            return sp
    	except Exception as e:
            raise CustomException(e, sys)
        
    def getData(self):
        try:
            logging.info('-----Data Ingestion Pipeline Initiated-----')
            
            dfBillboards = Billboards_Hot100_Chart(1946, 2022)
            dfBillboards.to_csv(config.wikipedia_data_path, index = False)
            logging.info('Scraped data of Billboard Hot 100 Chart from Wikipedia.\nStored in /data directory.')
            
            sp = getSpotifyInstance()
            dfBillboardsWithURI = addURIColumn(dfBillboards, sp)
            logging.info('Acquired Spotify URI of scraped songs using API.')
            
            final_data = Spotify_Features(dfBillboardsWithURI, sp)
            final_data.to_csv(config.spotify_data_path, index = False)
            logging.info('Downloded required metadata & audio features of all songs.\nStored in /data directory.')
            return final_data
        except Exception as e:
            raise CustomException(e, sys)