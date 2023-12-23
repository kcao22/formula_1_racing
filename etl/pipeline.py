import boto3
import loggers
import logging
import os

# from airflow import DAG
# from airflow.operators.python_operator import PythonOperator
# from airflow.operators.bash import BashOperator
# from datetime import datetime

from aws_classes import loader
from etl import extract
from etl import load

logger = logging.getLogger(__name__)

# # Extract and load to S3
# logger.info("Starting pipeline process. Extract process start.")
# list_csv_objs = [file for file in os.listdir("/mnt/d/Documents/Data Projects/formula_1_racing/data") if file.endswith('.csv')]
# extract.extract_to_s3(bucket="kc-f1-racing-landing", list_csv_objs=list_csv_objs)

# Load to RDS
logger.info("Beginning load to RDS process.")
load.glue_load_job(job_name="f1_racing_glue_s3_to_rds_nb")

# Call dbt commands
