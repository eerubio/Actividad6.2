"""
Module for handling JSON data.

Libraries:
- json: Provides functions for reading and writing JSON data.
"""
import json


class JSONDataHandler:
    """
    A class for handling JSON data.

    Attributes:
    - filename (str): The filename for storing JSON data. Defaults to
    'hotels.json'.

    Methods:
    - load_data: Loads JSON data from the specified file.
    - save_data: Saves JSON data to the specified file.
    """
    def __init__(self, filename='hotels.json'):
        """
        Initializes a JSONDataHandler object with the specified filename.

        Parameters:
        - filename (str, optional): The filename for storing JSON data.
        Defaults to 'hotels.json'.
        """
        self.filename = filename

    def load_data(self):
        """
        Loads JSON data from the specified file.

        Returns:
        The loaded JSON data.
        """
        with open(self.filename, 'r', encoding='UTF-8') as file:
            return json.load(file)

    def save_data(self, data):
        """
        Saves JSON data to the specified file.

        Parameters:
        - data: The JSON data to be saved.
        """
        with open(self.filename, 'w', encoding='UTF-8') as file:
            json.dump(data, file, indent=4)