resource "aws_subnet" "public" {
  count = var.enable_public_subnet && var.public_subnet_cidr != null ? 1 : 0

  vpc_id                  = aws_vpc.this.id
  cidr_block              = var.public_subnet_cidr
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.name}-public-subnet"
  }
}

resource "aws_subnet" "private" {
  for_each = {
    for idx, subnet in var.private_subnets :
    idx => subnet
  }

  vpc_id            = aws_vpc.this.id
  cidr_block        = each.value.cidr
  availability_zone = each.value.availability_zone

  tags = {
    Name = "${var.name}-private-${each.key}"
  }
}