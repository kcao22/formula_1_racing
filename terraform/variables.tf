variable "region" {
  type      = string
  sensitive = true
}

variable "access_key" {
  type      = string
  sensitive = true
}

variable "secret_key" {
  type      = string
  sensitive = true
}

variable "account_id" {
  type = string
  sensitive = true
}

variable "bucket_name" {
  type      = string
  sensitive = true
}

variable "rds_dbname" {
  type = string
  sensitive = true
}

variable "rds_username" {
  type      = string
  sensitive = true
}

variable "rds_password" {
  type      = string
  sensitive = true
}
