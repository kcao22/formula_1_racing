# Imports
import boto3
import loggers
import logging
import os

from api import ergast_api
from aws_classes import loader

logger = logging.getLogger(__name__)

def extract_to_s3(bucket: str, list_csv_objs: list):
    """
    Calls Ergast API to extract all data to S3 bucket.
    
    Args:
        bucket: S3 bucket to put CSV objects into.
        list_csv_objs: The list of CSV objects to put into S3 bucket.
    Returns:
        None
    """
    extract = ergast_api.ErgastAPI()
    extract.get_all_data("/mnt/d/Documents/Data Projects/formula_1_racing/data")
    load = loader.Loader()
    load.load_csv_objects(dir_path="./data/", files=list_csv_objs, bucket=bucket)
    logger.info("Loading process completed, all CSV files put into S3 bucket. Beginning Lambda function and Glue job.")