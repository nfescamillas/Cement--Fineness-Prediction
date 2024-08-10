terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = "us-east-1"
}

resource "aws_instance" "mlflow_server" {
  ami           = "ami-04a81a99f5ec58529"
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.network-security-group.id]

  tags = {
    Name = "mlflow-server"
  }
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


resource "aws_s3_bucket" "models" {
  bucket = "millproject-models-tf"

  tags = {
    Name        = "millproject-models-tf"
    Environment = "Dev"
  }
}

resource "aws_elastic_beanstalk_application" "fineness-prediction-serving" {
  name        = "fineness-prediction-serving-tf"
  
}

resource "aws_elastic_beanstalk_environment" "tfenvtest" {
  name                = "mill-project-serving"
  application         = aws_elastic_beanstalk_application.fineness-prediction-serving.name
  solution_stack_name = "64bit Amazon Linux 2 v4.0.0 running Docker"
}