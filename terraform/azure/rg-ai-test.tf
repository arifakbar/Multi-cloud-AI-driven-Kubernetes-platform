resource "azurerm_resource_group" "testing-ai-rg" {
    name     = "rg-ai-test"
    location = var.location
}