# Imports
import os
import logging 
from aws_session import AWSSession

logger = logging.getLogger(__name__)

class Loader():
    """
    Creates Loader object.
    """
    def __init__(self, bucket: str):
        """
        Instantiates Loader object.
        """
        self.bucket_name = bucket
        self.session = AWSSession()

    def load_csv_objects(self, dir_path: str, files: list):
        """
        Loads all CSV files to S3 bucket.
        
        Args:
            dir_path: Specifies where to look for CSV objects.
            files: List of CSV objects to put to S3 bucket.
            bucket_name: AWS S3 bucket to put objects into.
        
        Returns:
            None
        """
        s3 = self.session.create_session("s3")
        for file in files:
            file_path = os.path.join(dir_path, file)
            with open(file_path, "rb") as data:
                try:
                    s3.put_object(
                        Bucket=self.bucket_name
                        , Key=file
                        , Body=data
                    )
                    logger.info(f"{file} has been put into S3 bucket.")
                except FileNotFoundError as e:
                    logger.exception(f"FileNotFoundError occurred: {e}")
                    raise