resource "aws_vpc" "vpc" {
  cidr_block = "10.1.0.0/16"
  tags = {
    Name = "vpc-multicloud"
  }
}

resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = "10.1.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "public-subnet"
  }
}
