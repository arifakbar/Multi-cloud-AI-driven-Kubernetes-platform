terraform {
  backend "s3" {
    bucket         = ""        # S3 bucket name
    key            = ""        # Path to state file (e.g., env/dev/terraformtfstate)
    region         = ""        # AWS region where bucket exists
    dynamodb_table = ""        # (Optional but recommended) for state locking
    encrypt        = true
  }
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.0.0"  # Adjust version as needed
    }
  }
}

provider "aws" {
  region = ""  # e.g., ap-south-1
}