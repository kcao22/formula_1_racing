# Imports
import datetime
import logging
import os
import requests
import shutil
import zipfile
from .generic_api import GenericAPI

logger = logging.getLogger(__name__)

class ErgastAPI(GenericAPI):
    """
    Instantiates ErgastAPI object. Inherits from GenericAPI class.
    """
    def __init__(self, url="http://ergast.com"):
        """
        Calls parent class ErgastAPI object contsructor to set base URL
        for object.
        """
        super().__init__(url)
        
        
    def get_historical_race_results(self, year_start: int, year_end: int):
        """
        Gets historical results between a given start year and a given 
        end year (inclusive).
        
        Args:
            year_start: Integer start year. Must be no earlier than 1950.
            year_end: Integer end year.
            
        Returns:
            List of JSON objects.
        """
        # Check arguments
        if (year_start < 1950 or year_end > datetime.datetime.now().year or year_start > year_end):
            logger.error(f"Year range error occurred: Year range {year_start} - {year_end} is an invalid year range.")
            raise ValueError("Year range must be between 1950 and current year. Please ensure year start is prior to year end.")
        else:
            logger.info(f"Requesting historical data from range {year_start} - {year_end}.")
            results = []
            if year_start == year_end:
                results.append(super().get(f"api/f1/{year_start}.json"))
            else:
                for year in range(year_start, year_end+1):
                    results.append(super().get(f"api/f1/{year}.json"))
            return results
    
    def get_latest_race_results(self):
        """
        Gets the latest race results.
        
        Args:
            None
            
        Returns:
            JSON object.
        """
        logger.info("Requesting latest race results.")
        return super().get("api/f1/current/last/results.json")

    def _check_delete_file(self, file_path: str):
        """
        Check to see if file exists. Delete if exists.
        
        Args:
            file_path: String representing directory where file should be
            saved to.
        Returns: 
            None
        """
        if os.path.exists(file_path):
            os.remove(file_path)

    def get_all_data(self, directory_path: str):
        """
        Requests all data, including lap times, pit stops, etc. in a 
        zipped archive. Files within the archive are of CSV format. Files
        will be saved to specified directory_path.
        
        Args:
            file_path: String representing directory where file should be
            saved to.
        Returns:
            None
        """
        # Check delete previously existing file
        file_path = f"{directory_path}/all_data.zip"
        self._check_delete_file(file_path)
        
        # Get data from API
        api_path = f"{self.base_url}/downloads/f1db_csv.zip"
        print(api_path)
        logger.info(f"API get request for path URL: {api_path}.")
        try:
            res = requests.get(api_path, stream=True)
        except requests.exceptions.HTTPError as e:
            logger.exception(f"HTTP Error occurred: {str(e)}")
            raise
        
        # Write zip to directory
        with open(file_path, "wb") as file:
            shutil.copyfileobj(res.raw, file)
        logger.info(f"Compressed archive downloaded to path: {file_path}. \nExtracting CSV files from zipped archive.")
        # Extract and save CSV files locally
        with zipfile.ZipFile(file_path, "r") as zip_file:
            for file in zip_file.namelist():
                if file.endswith(".csv"):
                    csv_path = f"{directory_path}/{file}"
                    self._check_delete_file(csv_path)
                    zip_file.extract(file, csv_path)
        logger.info(f"All CSV files extracted.")