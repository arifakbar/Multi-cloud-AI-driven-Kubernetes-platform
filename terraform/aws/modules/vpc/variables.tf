variable "name" {
  description = "Name prefix for resources"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
}

variable "public_subnet_cidr" {
  description = "CIDR block for public subnet"
  type          = string
  default     = null
}

variable "private_subnets" {
  description = "List of private subnets"
  type = list(object({
    cidr              = string
    availability_zone = string
  }))
}

# variable "availability_zone" {
#   description = "Availability zone"
#   type        = string
# }

variable "enable_public_subnet" {
  description = "Create public subnet"
  type        = bool
  default     = false
}

variable "enable_nat_gateway" {
  description = "Create NAT gateway"
  type        = bool
  default     = false
}

variable "enable_internet_gateway" {
  description = "Create Internet Gateway"
  type        = bool
  default     = false
}