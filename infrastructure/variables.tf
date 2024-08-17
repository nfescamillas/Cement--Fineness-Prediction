variable "aws_region" {
 description = "AWS region to create resources"
 default = "eu-east-1" 
}

variable "project_id" {
 description = "project id"
 default = "cement-fineness-project" 
}

variable "bucket_name" {
  description = "bucket name for model artifacts and registry"
  default = "fineness-prediction-models-tf"
}

