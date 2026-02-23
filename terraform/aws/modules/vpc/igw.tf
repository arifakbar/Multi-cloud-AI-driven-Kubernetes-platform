resource "aws_internet_gateway" "igw" {
  count  = var.enable_internet_gateway ? 1 : 0
  vpc_id = aws_vpc.this.id

  tags = {
    Name = "${var.name}-igw"
  }
}