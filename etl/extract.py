# Imports
import boto3
import loggers
import logging
import os

from api import ergast_api
from aws_classes import loader

logger = logging.getLogger(__name__)

def extract_to_s3(bucket: str):
    """
    Calls Ergast API to extract all data to S3 bucket.
    
    Args:
        bucket: S3 bucket to put CSV objects into.
    Returns:
        None
    """
    logger.info("Extract to S3 process beginning.")
    extract = ergast_api.ErgastAPI()
    extract.get_all_data("/mnt/d/Documents/Data Projects/formula_1_racing/data")
    load = loader.Loader()
    # Set list CSV files to load
    list_csv_objs = [file for file in os.listdir("/mnt/d/Documents/Data Projects/formula_1_racing/data") if file.endswith('.csv')]
    load.load_csv_objects(dir_path="./data/", files=list_csv_objs, bucket=bucket)
    logger.info("Loading process completed, all CSV files put into S3 bucket. Beginning Lambda function and Glue job.")