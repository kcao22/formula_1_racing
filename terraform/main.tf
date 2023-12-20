terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.31.0"
    }
  }
}

provider "aws" {
  # Configuration options
  region = var.region
}

# Create landing bucket
resource "aws_s3_bucket" "landing_bucket" {
  bucket        = var.bucket_name
  force_destroy = true
  tags = {
    Name = "Landing Bucket"
  }
}

# Create IAM Role for Lambda Function
resource "aws_iam_role" "lambda_role" {
  name = "f1_racing_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

# Create S3 read write policy for lambda role
resource "aws_iam_policy" "s3_rw_policy" {
  name        = "s3_rw_policy"
  description = "S3 read and write permissions."
  policy      = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "ListObjectsInBucket",
        "Effect": "Allow",
        "Action": ["s3:ListBucket"],
        "Resource": ["arn:aws:s3:::${var.bucket_name}/*"]
      },
      {
        "Sid": "AllObjectActions",
        "Effect": "Allow",
        "Action": "s3:*Object",
        "Resource": ["arn:aws:s3:::${var.bucket_name}/*"]
      }
    ]
  }
  EOF
}

# Attach S3 read write policy for lambda role
resource "aws_iam_role_policy_attachment" "lambda_s3_rw_access" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.s3_rw_policy.arn
}

# Create S3 Event Access policy to access bucket from S3 events
resource "aws_iam_policy" "s3_access_policy" {
  name        = "lambda_s3_access_policy"
  description = "S3 access policy for Lambda function"
  policy      = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ],
        "Resource": "arn:aws:s3:::${var.bucket_name}/*"
      }
    ]
  }
  EOF
}

# Attach S3 Event Access policy to lambda role
resource "aws_iam_role_policy_attachment" "s3_access_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.s3_access_policy.arn
}

# Create lambda function
resource "aws_lambda_function" "lambda_function" {
  filename      = "lambda_function_payload.zip"
  function_name = "f1_racing_lambda"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "python3.9"
}

# Create S3 bucket notification for object creations, puts, etc.
# Filter for .csv files only
resource "aws_s3_bucket_notification" "s3_bucket_notification" {
  bucket = aws_s3_bucket.landing_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.lambda_function.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".csv"
  }
}

# Allow bucket to trigger lambda function upon object creation event
resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_function.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.landing_bucket.arn
}

# Deploy RDS instance
resource "aws_db_instance" "rds_sqlserver_db" {
  allocated_storage    = 20
  db_name              = var.rds_dbname
  engine               = "sqlserver-ex"
  engine_version       = "15.00.4335.1.v1"
  instance_class       = "db.t3.micro"
  username             = var.rds_username
  password             = var.rds_password
  parameter_group_name = "default.sqlserver-ex-15.0"
  publicly_accessible  = true
  skip_final_snapshot  = true
}

# Create glue role
resource "aws_iam_role" "glue_role" {
  name = "f1_racing_glue_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      },
    ]
  })
}

# Create policy to give glue access to RDS database.
resource "aws_iam_policy" "glue_rds_policy" {
  name        = "glue_rds_policy"
  description = "RDS access policy for Glue job"
  policy      = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "VisualEditor0",
        "Effect": "Allow",
        "Action": [
          "rds:DescribeDBInstances",
          "rds:ExecuteStatement"
        ],
        "Resource": "${aws_db_instance.rds_sqlserver_db.arn}"
      }
    ]
  }
  EOF
}

# Attach glue rds policy to glue role
resource "aws_iam_role_policy_attachment" "glue_rds_access" {
  role       = aws_iam_role.glue_role.name
  policy_arn = aws_iam_policy.glue_rds_policy.arn
}

# Create lambda to glue access policy
resource "aws_iam_policy" "lambda_glue_policy" {
  name        = "f1_racing_lambda_glue_policy"
  description = "Glue access policy for Lambda function"
  policy      = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "VisualEditor0",
        "Effect": "Allow",
        "Action": [
          "glue:StartJobRun",
          "glue:GetJobRun",
          "glue:BatchStopJobRun",
          "glue:GetJobRuns"
        ],
        "Resource": "*"
      }
    ]
  }
  EOF
}

# Attach 
resource "aws_iam_role_policy_attachment" "lambda_glue_access" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_glue_policy.arn
}



# # Create glue job
# resource "aws_glue_job" "glue_write_job" {
#   name     = "f1_racing_write_to_rds"
#   role_arn = aws_iam_role.glue_role.arn

#   command {
#     script_location = "s3://my-script-bucket/example_script.py"
#     name            = "glueetl"
#   }
# }