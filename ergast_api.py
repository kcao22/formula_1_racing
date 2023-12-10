# Imports
import logging
import requests
from generic_api import GenericAPI

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
        if year_start > year_end:
            logger.error(f"Year range error occurred: {year_start} is 
                         later than {year_end}. Did you mean to reverse
                         the year arguments?")
        if year_start < 1950:
            logger.error(f"ErgastAPI tracks ")
        results = []
        try:
            for year in range(year_start, year_end+1):
                super().get()
        except 