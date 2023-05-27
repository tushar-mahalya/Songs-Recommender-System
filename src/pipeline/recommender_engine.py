import os
import pandas as pd
import sys
import json
from src.exception import CustomException
from src.logger import logging
from config import ROOT_DIR

from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    data_path: str = ROOT_DIR + '/data/[Spotify]_Billboard_Hot100_Songs_1946-2022.csv'
if __name__ == '__main__':
    config = DataIngestionConfig()
    data = pd.read_csv(config.data_path)
    print('Data Read')