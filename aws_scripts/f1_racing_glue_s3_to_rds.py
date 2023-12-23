# Set job parameters using magic
%idle_timeout 2880
%glue_version 4.0
%worker_type G.1X
%number_of_workers 5
%connections F1RacingSQLServer

# Imports
import boto3
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from botocore.exceptions import NoCredentialsError

# Set spark context and glue context
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# Create S3 client
s3 = boto3.client("s3")

# Get CSV objects
bucket_res = s3.list_objects_v2(Bucket="kc-f1-racing-landing")
list_csv_objects = [file["Key"] for file in bucket_res["Contents"] if file["Key"].endswith(".csv")]

# For each CSV: check if corresponding table exists in RDS DB, load table
# if not exists. If table exists, append new data to existing table.
for file in list_csv_objects:
    ddf = glueContext.create_dynamic_frame.from_options(
        connection_type="s3",
        connection_options={"paths": [f"s3://kc-f1-racing-landing/{file}"]},
        format="csv",
        format_options={"withHeader": True}
    )
    df = ddf.toDF()
    table_name = file.replace(".csv", "")
    try:
        ddf_old = glueContext.create_dynamic_frame.from_options(connection_type = 
        "custom.jdbc", connection_options = {"dbTable": table_name,"connectionName":"F1RacingSQLServer"}, transformation_ctx = "DataSource0")
        df_old = ddf_old.toDF()
    except Exception as e:
        df_old = spark.createDataFrame([], df.schema).limit(0)
    # Update and append new data and overwrite existing table.
    diff_df = df.subtract(df_old)
    updated_df = df.unionAll(diff_df)
    updated_ddf = DynamicFrame.fromDF(updated_df, glueContext, "updated_ddf")
    glueContext.write_dynamic_frame.from_jdbc_conf(
        frame=updated_ddf,
        catalog_connection="F1RacingSQLServer",
        connection_options={
            "database": "Raw",
            "dbtable": table_name
        }
    )
    print(f"Overwriting existing table {file.replace('.csv', '')} within RDS")