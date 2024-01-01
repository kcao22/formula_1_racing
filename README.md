# Formula 1 Racing ETL Pipeline - Winningest Constructors and Drivers All Time

**ELT Pipeline Process**:
![Alt Text](https://github.com/kcao22/formula_1_racing/blob/main/diagrams/Formula%201%20Racing%20ELT.png)

**Demo of Final Power BI Dashboard**:
![Alt Text](https://github.com/kcao22/formula_1_racing/blob/main/diagrams/dashboard_demo.gif)

**Dimensional Model Design**:
![Alt Text](https://github.com/kcao22/formula_1_racing/blob/main/diagrams/formula_1_racing_dimensional_model.png)

## Source Data
 - Ergast API:
     - https://ergast.com/mrd/

## Project Goals
 - Follow SDLC best practices (OOP, Continuous Integration, Logging) and build a robust, fault-tolerant pipeline.
 - Create wrapper classes for reuseable and user friendly extract and load processes.
 - Explore, design, and implement Terraform IaC configurations with AWS Cloud Computing Services.
 - Automate and orchestrate modern data pipeline infrastructure with Apache Airflow.
   
## Libraries and Resources Used
 - **Python Version**: 3.11
 - **Main Packages**: Apache Airflow, boto3, dbt, logging, requests
 - **Resources**: AWS Cloud Computing Services, Terraform

# Pipeline Architecture and Process
## Source Data, Extract and Load - Python Object Oriented Programming (APIs and AWS boto3)
 1. Used Python object oriented programming to write custom classes for extract and load process. The goal was to demonstrate building generalized classes, and then utilizing object oriented programming principles like inheritance and composition to build classes with more specific functionality.
 2. Pulled historical datasets from Ergast API and unzipped files locally. Based on CSV files extracted from .zip archive, CSV files were uploaded to AWS S3 landing bucket.

## Logging and Continuous Integration - Python Logging Configuration and GitHub Actions
 1. To best handle pipeline failures, I configured a default logger configuration and implemented logging information, exception, and error handling with messages throughout each step of the ELT process. This was done via Python's built in logging library and creating logger instances within the extract and load classes I had written to write to an ELT pipeline log specified within the code.
 2. Within the logs, debug information as well as any exception and errors caught and raised within the code were all available for reading and use upon failures or issues that popped up during execution of the extract and load phases.
 3. To fully test my custom classes and associated methods with each class, I wrote unit tests using pytest and its built in features such as pytest.fixture Python decorators. In doing so, unit tests were not redundantly instantiating objects and were also tested for proper functionality.
 4. GitHub Actions was then employed to execute the unit tests upon each push to the remote repository.
 5. PEP 8 style was followed for custom classes, although logging messages would sometimes be longer than the suggested PEP 8 style. 

## Deployment - Terraform IaC with AWS
 1. One of the main goals of this project was to explore the use of Terraform and deployment of cloud infrastructure for easier management (deployment, modification, and destruction of services).
 2. To keep the pipeline in line with more modern designs (data lake, ETL/ELT jobs, and cloud databases), I wrote a Terraform configuration file to deploy a S3 bucket, a RDS SQL Server instance, and a Glue job to move raw data from the data lake to the RDS as part of the ELT design.
 3. All necessary IAM policies and roles necessary for the operation of the ELT pipeline were also configured via Terraform with the principle of least privilege in mind (Glue read access to S3, Glue read write access to RDS, etc.).
 4. AWS lambda function was considered for triggering of Glue load to RDS job upon detection of CSV file upload to S3 bucket, but was ultimately removed from the pipeline in favor of using Apache Airflow for more robust step-by-step orchestration via DAGs. In the case of failures, I wanted to see the failure within my pipeline log as well as within my Airflow visual DAG diagram.
 
## Load Raw - RDS SQL Server Instance 
 1. To further expand my experience with AWS services, I chose to use AWS RDS as my cloud database for loading and transforming data. Because the raw data was small in volume, a smaller instance type of AWS RDS was selected for this pipeline. However, by architecting this pipeline as an ELT design, it was important to manage the performance tier of the RDS instance. Although the data volume was small, it was still necessary to scale the performance tier as needed (e.g. t3.micro to t3.medium).
 2. A PySpark glue job was used to connect to the RDS instance and compare data to existing data within the RDS database. If new data was appended to the F1 racing datasets, then the glue job would take the difference in data rows between the existing dataset within the RDS raw schema tables and the currently newly loaded raw data within S3 and append the difference in data to the existing dataset within the RDS raw tables. Because the data is historical and the data source states that historical data is very unlikely to change, any backloading or refreshing of data was not considered. This incremental loading process was performed to reduce full dataset reloading to RDS database tables, thus conserving costs.
 3. All security group implementations and routing accessibility for connecting to the RDS instance were configured via AWS console. As in line with the principle of least privilege, all connection operations were performed following AWS's robust documentation on connectivity.

## Transformation and Schema Design - dbt
 1. As mentioned above, the ELT process focused on incrementally loading new data to the RDS database raw schema tables as soon as new race data is available. dbt was then chosen as the transform tool to design a dimensional model that would serve my purpose and answer my questions on who the greatest formula 1 racers are and which companies have the most wins in the industry.
 2. To create a dimensional model design to fulfill my analytics questions, I chose to focus on designing a fact table that recorded race results by constructor and driver. The granularity of the table therefore would capture the race results and associated metrics along with the results (points earned, total laps raced, etc.).
 3. dbt features such as incremental materialization, seeding for static dimension tables, and custom model testing using dbt.utils were implemented to test for primary key uniqueness, duplicate checks, and null values.

## Dashboard Visualization - Power BI
 1. Power BI offers clean integration with SQL Server databases and was chosen for this project.
 2. Further, Power BI can ingest well modeled star schema models such as the one designed for this project via dbt. In this way, relational dimensional models can be seamlessly used within Power BI to generate dynamic visuals.
 3. To answer my analytical questions, historical performance via circuit points earned and also high-level KPI cards were implemented on the first tabs of the Power BI dashboard to show summarized performances (total wins, total top 3 finishes, total top grid position starts, etc.). Users can further filter on car manufacturer / constructor and visualize the performance of companies or drivers over time. Finally, visuals for top records of all time for different racing metrics (total laps raced, total top 3s, total wins, etc.) were implemented in the final two dashboard pages. See the above GIF for a demonstration of the dashboard functionality.

## Orchestration - Apache Airflow
 1. As previously stated, Apache Airflow was chosen for more automated, robust, step-by-step handling of the pipeline process (executing extract and load operations via interactions with AWS services and local classes as well as execution, testing, and building of dimensional models via dbt).
 2. Airflow Python operators were chosen to execute ELT functions and Bash operators were chosen to execute dbt commands for debugging, testing, and building.
 3. Email notifications were set up for notification of failed DAG steps.
