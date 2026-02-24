module "prod_vpc" {
  source = "./modules/vpc"

  name     = "prod"
  vpc_cidr = "10.20.0.0/16"

  # Enable optional resources
  enable_public_subnet    = true
  enable_internet_gateway = true
  enable_nat_gateway      = true

  # Public subnet (single – NAT lives here)
  public_subnet_cidr = "10.20.1.0/24"
  public_subnet_az   = "us-east-1a"

  # Private subnets (multi-AZ production)
  private_subnets = [
    {
      cidr              = "10.20.10.0/24"
      availability_zone = "us-east-1a"
    },
    {
      cidr              = "10.20.11.0/24"
      availability_zone = "us-east-1b"
    }
  ]
}