resource "aws_s3_bucket" "model" {
  bucket = var.bucket_name
  tags =var.tags
}