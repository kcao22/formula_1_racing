variable "region" {
  type      = string
  sensitive = true
}

variable "account_id" {
  type      = string
  sensitive = true
}

variable "bucket_name" {
  type      = string
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

variable "rds_hostname" {
  type      = string
  sensitive = true
}

variable "rds_port" {
  type      = string
  sensitive = true
}

variable "rds_db" {
  type      = string
  sensitive = true
}
