import os
import sys
import json
from src.exception import CustomException
from src.logger import logging

from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    billboards_info_file_path: str = 'resources/BillboardHot100(1958-2021).csv'
class DataIngestion:

    def __init__(self):
        self.ingestion_config = DataIngestionConfig()