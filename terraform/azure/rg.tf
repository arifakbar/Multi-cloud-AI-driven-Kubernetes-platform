resource "azurerm_resource_group" "test-rg" {
  name     = "test-rg"
  location = var.location
}