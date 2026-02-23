resource "azurerm_resource_group" "test-rg" {
  name     = "rg-multicloud"
  location = var.location
}