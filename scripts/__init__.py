# Initialization code
print("Initializing the scripts package")

# Import necessary modules and functions
from .data_processor import data, process_data
from .reddit_scrapper import data, process_data
from .sentiment_analyzer import data, process_data
from read_db import data, process_data

# Define what is available when the package is imported
__all__ = ['data', 'process_data']
