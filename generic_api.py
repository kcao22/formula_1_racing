import logging
import requests

logger = logging.getLogger(__name__)

class GenericAPI():
    """
    Creates generic API object. Acts as a base class for all API classes
    that inherit this class.
    """
    def __init__(self, url: str):
        """
        Instantiates GenericAPI object. Sets base URL for object.
        
        Args:
            url: The base URL for an API request.
            
        Returns:
            None
        """
        self.base_url = url
        
    def get(self, path_parameter: str):
        """
        Appends argument path to base URL and performs get request.
        
        Args:
            path_parameter: Path parameter string that appends to base 
            URL path before request action is sent. 
                Example: "current/last/results"
        
        Returns:
            Requested data as JSON object.
        """
        url = f"{self.base_url}/{path_parameter}"
        response = requests.get(url)
        logger.info(f"API get request sent for path URL: {url}.")
        try:
            # Check request status code
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.exception(f"HTTP Error occurred: {str(e)}")
            # Catch last exception active within current scope
            # Re-raise exception after logging
            raise
        else:
            logger.info("Successfully returning JSON object.")
            return response.json()