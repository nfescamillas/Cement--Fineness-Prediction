resource "aws_elastic_beanstalk_environment" "fineness-prediction-serving-env" {
  name                = "fineness-prediction-serving-env-tf"
  application         = var.application
  solution_stack_name = var.platform_type
  tags = var.tags
}

output "name"{
  value = aws_elastic_beanstalk_environment.fineness-prediction-serving-env.name
}