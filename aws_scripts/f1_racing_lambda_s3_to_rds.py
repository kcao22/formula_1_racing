import boto3

def lambda_handler(event, context):
    """
    Lambda function to run glue job that moves uploaded CSV data from S3 
    bucket to RDS instance.
    """
    glue = boto3.client("glue")
    glue_job_name = "f1_racing_glue_s3_to_rds"
    try:
        job_run_id = glue.start_run_job(JobName=glue_job_name)
        res_status = glue.get_job_run(JobName=glue_job_name, RunId=job_run_id["JobRunId"])
        return res_status["JobRun"]["JobRunState"]
    except Exception as e:
        print(e)
        raise