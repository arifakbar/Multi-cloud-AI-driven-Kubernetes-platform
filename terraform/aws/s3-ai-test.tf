resource "aws_s3_bucket" "testing_ai" {
  bucket = "ai-test-bucket-unique-123456"
    
  tags = {
    Name    = "ai-test"
    Project = "ai-test"
  }
}