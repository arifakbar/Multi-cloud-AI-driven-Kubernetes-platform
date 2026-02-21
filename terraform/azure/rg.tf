resource "azurerm_resource_group" "rg-test" {
  name     = "test-rg"
  location = var.location
}