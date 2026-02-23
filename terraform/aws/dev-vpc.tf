module "dev_vpc" {
  source = "./modules/vpc"

  name     = "dev"
  vpc_cidr = "10.10.0.0/16"

  enable_public_subnet    = false
  enable_internet_gateway = false
  enable_nat_gateway      = false

  private_subnets = [
    {
      cidr              = "10.10.1.0/24"
      availability_zone = "us-east-1a"
    }
  ]
}