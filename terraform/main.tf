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
  access_key = var.access_key
  secret_key = var.secret_key
  region = var.region
}

resource "aws_s3_bucket" "example" {
  bucket = var.bucket_name
  force_destroy = true
  tags = {
    Name        = "Landing Bucket"
  }
}

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

resource "aws_iam_policy" "s3_rw_policy" {
  name = "s3_rw_policy"
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

resource "aws_iam_role_policy_attachment" "lambda_s3_rw_access" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.s3_rw_policy.arn
}

resource "aws_db_instance" "rds_sqlserver_db" {
  allocated_storage    = 20
  db_name              = var.rds_dbname
  engine               = "sqlserver-ex"
  engine_version       = "15.00.4335.1.v1"
  instance_class       = "db.t3.micro"
  username             = var.rds_username
  password             = var.rds_password
  parameter_group_name = "default.mysql5.7"
  publicly_accessible = true
  skip_final_snapshot  = true
}

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

resource "aws_glue_job" "glue_write_job" {
  name     = "f1_racing_write_to_rds"
  role_arn = aws_iam_role.glue_role.arn

  command {
    script_location = "s3://my-script-bucket/example_script.py"
    name            = "glueetl"
  }
}
