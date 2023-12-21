# Imports
import boto3
import configparser
import logging
import os

logger = logging.getLogger(__name__)

class AWSSession():
    """
    Creates AWSSession object.
    """
    def __init__(self):
        """
        Instantiates Loader object.
        """
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "credentials.config"))
        self.access_key = self.config.get("AWS", "aws_access_key")
        self.secret_key = self.config.get("AWS", "aws_secret_key")
        self.region = self.config.get("AWS", "region")
    
    def create_session(self, aws_service: str):
        """
        Creates boto3 session object for a specific AWS service.
        
        Args:
            aws_service: Specific service to create session object for.
        
        Returns:
            boto3 Session object.
        """
        logger.info("Creating boto3 session object.")
        session = boto3.Session(
            aws_access_key_id=self.access_key
            , aws_secret_access_key=self.secret_key
            , region_name=self.region 
        )
        return session.client(aws_service)