resource "aws_s3_bucket" "high_severity_bucket" {
  bucket = "ai-high-severity-bucket-123456"

  # 🚨 HIGH - Public ACL
  acl = "public-read"

  # 🚨 LOW - Versioning disabled
  versioning {
    enabled = false
  }

  tags = {
    Name = "high-severity-bucket"
  }
}

# 🚨 MEDIUM - Policy attached
resource "aws_s3_bucket_policy" "public_policy" {
  bucket = aws_s3_bucket.high_severity_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = "*"
        Action = "s3:GetObject"
        Resource = "${aws_s3_bucket.high_severity_bucket.arn}/*"
      }
    ]
  })
}