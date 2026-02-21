terraform {
  backend "azurerm" {
    resource_group_name = "initial-tf-rg"
    storage_account_name = "terraformx123"
    container_name       = "terraform"
    key                  = "terraform.tfstate"
  }
}

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.61.0"
    }
  }
}
