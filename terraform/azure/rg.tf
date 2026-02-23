resource "azurerm_resource_group" "rg" {
  name     = "rg-multicloud"
  location = var.location
}