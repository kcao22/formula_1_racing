# Imports
import datetime
import logging
import requests
from .generic_api import GenericAPI

logger = logging.getLogger(__name__)

class ErgastAPI(GenericAPI):
    """
    Instantiates ErgastAPI object. Inherits from GenericAPI class.
    """
    def __init__(self, url="http://ergast.com/api/f1"):
        """
        Calls parent class ErgastAPI object contsructor to set base URL
        for object.
        """
        super().__init__(url)
        
        
    def get_historical_results(self, year_start: int, year_end: int):
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
                results.append(super().get(f"{year_start}.json"))
            else:
                for year in range(year_start, year_end+1):
                    results.append(super().get(f"{year}.json"))
            return results
    
    def get_latest_results(self):
        """
        Gets the latest race results.
        
        Args:
            None
            
        Returns:
            JSON object.
        """
        logger.info("Requesting latest race results.")
        return super().get("current/last/results.json")
