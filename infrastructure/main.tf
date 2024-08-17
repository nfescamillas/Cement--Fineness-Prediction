terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
# Manually create the state bucket
  required_version = ">= 1.2.0"
  backend "s3"{
    bucket = "cement-fineness-project-tf"
    key = "cement-fineness-stg.tfstate"
    region = var.aws_region
    encrypt = true
  }
}
# provider block helps add a predefined resource type and resources 
provider "aws" {
  region  = var.aws_region
}

data "aws_caller_identity" "current_identity" {}

locals {
  account_id = data.aws_caller_identity.current_identity.account_id
}

resource "aws_security_group" "network-security-group" {
  name        =  "Mlflow Server SG"
  description = "Allow TLS inbound traffic"

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
    }

   ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
    }

   ingress {
    description = "Custom TCP"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
    }
}

module "mlflow_tracking_server" {
  source = "./modules/ec2"
  vpc_security_group_ids = aws_security_group.network-security-group
  tags = var.project_id
}

module "model_registry" {
  source = "./modules/s3"
  bucket_name = var.bucket_name
  tags =var.project_id
  
}

module "eb_app"{
  source = "./modules/eb-app"
  tags= var.project_id
}

module "eb_env"{
  source = "./modules/eb-env"
  application = module.eb_app.name
  tags=var.project_id
}

output "eb_application" {
  value = module.eb_app.name
}

output "eb_environment" {
  value =module.eb_env.name
}