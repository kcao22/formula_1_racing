import loggers
import logging
import time

import boto3.exceptions

from aws_classes import aws_session

logger = logging.getLogger(__name__)

def glue_load_job(job_name: str):
    """
    Starts glue job to load CSV data to RDS.
    
    Args:
        job_name: Glue job to run
    Returns:
        None
    """
    logger.info("Beginning ")
    session = aws_session.AWSSession()
    glue = session.create_session("glue")
    try:
        res = glue.start_job_run(JobName=job_name)
        logger.info(f"Glue Job {job_name} successfully started with JobRunId {res['JobRunId']}.")
        # Logic to wait for glue job to finish and check status of run
        while True:
            status = glue.get_job_run(JobName=job_name, RunId=res["JobRunId"])["JobRun"]["JobRunState"]
            if status in ("FAILED", "STOPPED"):
                logger.error(f"Glue Job {job_name} failed with JobRunId {res['JobRunId']}.")
                break
            elif status == "SUCCEEDED":
                logger.info(f"Glue Job {job_name} successfully completed with JobRunId {res['JobRunId']}.")
                break
            else:
                # If the job is still running, wait 5 seconds
                time.sleep(5)
    except boto3.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "EntityNotFoundException":
            logger.exception(f"Job not found: {e}")
            raise
        else:
            logger.exception(f"boto3 client error in run_glue_job: {e}")
            raise
    except boto3.exceptions.BotoCoreError as e:
        logger.exception(f"Unexpected error in run_glue_job: {e}")
        raise