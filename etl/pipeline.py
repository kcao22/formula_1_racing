import boto3
import loggers
import logging
import os

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

from etl import extract
from etl import load

# Instantiate logger
logger = logging.getLogger(__name__)

# Instantiate objects




default_args = {
    "owner": "" 
}

with DAG(
    dag_id="formula1_etl",
    default_args=default_args,
    schedule_interval=datetime.timedelta(days=1)
) as f1_dag:
    task_extract = PythonOperator(
        task_id="extract_load_to_s3",
        python_callable=extract.extract_to_s3,
        op_kwargs={
            "bucket": "kc-f1-racing-landing"
        }
    )

    task_load = PythonOperator(
        task_id="glue_load_to_rds",
        python_callable=load.glue_load_job,
        op_kwargs={
            "job_name": "f1_racing_glue_s3_to_rds_nb"
        }
    )
    
    task_dbt_transform_A = BashOperator(
        task_id="check_rds_connection",
        bash_command=
        '''
        cd /mnt/d/Documents/Data\ Projects/formula_1_racing/formula_1_racing
        dbt debug
        '''
    )
    
    task_dbt_transform_B = BashOperator(
        task_id="test_dbt_source_data",
        bash_command='''
        cd /mnt/d/Documents/Data\ Projects/formula_1_racing/formula_1_racing
        dbt test --select source:*
        '''
    )
    
    task_dbt_transform_C = BashOperator(
        task_id="build_dbt_stg_models",
        bash_command='''
        cd /mnt/d/Documents/Data\ Projects/formula_1_racing/formula_1_racing
        dbt run --models staging.*
        '''
    )
    
    task_dbt_transform_D = BashOperator(
        task_id="test_dbt_stg_models",
        bash_command='''
        cd /mnt/d/Documents/Data\ Projects/formula_1_racing/formula_1_racing
        dbt test --models staging.*
        '''
    )
    
    task_dbt_transform_E = BashOperator(
        task_id="build_dbt_mart_models",
        bash_command='''
        cd /mnt/d/Documents/Data\ Projects/formula_1_racing/formula_1_racing
        dbt run --models marts.*
        '''
    )
    
    task_dbt_transform_F = BashOperator(
        task_id="test_dbt_mart_models",
        bash_command='''
        cd /mnt/d/Documents/Data\ Projects/formula_1_racing/formula_1_racing
        dbt test --models marts.*
        '''
    )

task_extract >> task_load >> task_dbt_transform_A >> task_dbt_transform_B >> task_dbt_transform_C >> task_dbt_transform_D >> task_dbt_transform_E >> task_dbt_transform_F