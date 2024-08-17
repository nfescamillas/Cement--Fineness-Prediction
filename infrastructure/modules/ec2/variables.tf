variable "ami"{
    description = "ami for the ec2 instance"
    default = "ami-04a81a99f5ec58529"
}

variable "instance_type" {
    description = "type of ec2 instance"
    default = "t2.micro"
}

variable "vpc_security_group_ids" {
    description = "allow inbound traffic"
  
}

variable "tags" {
    description = "tag for ec2 instance"
  
}