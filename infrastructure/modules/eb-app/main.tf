resource "aws_elastic_beanstalk_application" "fineness-prediction-serving" {
  name        = "fineness-prediction-serving-tf"
  tags = var.tags
}


output "name"{
  value = aws_elastic_beanstalk_application.fineness-prediction-serving.name
}
