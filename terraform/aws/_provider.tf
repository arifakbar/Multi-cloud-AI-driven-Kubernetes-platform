terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.33.0"
    }
  }
  backend "s3" {
    bucket         = "terraformx-aws"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-lock"
  }
}

//arn:aws:iam::007222077088:role/Github-Actions

provider "aws" {
  region = var.region # Authentication via OIDC is handled in GitHub Actions, no keys here
}