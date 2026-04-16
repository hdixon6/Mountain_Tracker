variable "aws_region" {
  type    = string
  default = "eu-west-2"
}

variable "app_name" {
  type    = string
  default = "mountain-tracker"
}

variable "db_name" {
  type    = string
  default = "mountaintracker"
}

variable "db_username" {
  type = string
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "github_connection_arn" {
  type = string
}

variable "github_repository_url" {
  type = string
}

variable "github_branch" {
  type    = string
  default = "main"
}

variable "db_subnet_ids" {
  type = list(string)
}
