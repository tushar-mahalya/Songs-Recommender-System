import os
import sys
import json
from src.exception import CustomException
from src.logger import logging

from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    data_path: str = '/data/[Spotify]_Billboard_Hot100_Songs_1946-2022.csv.csv'