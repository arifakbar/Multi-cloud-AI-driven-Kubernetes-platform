resource "azurerm_resource_group" "rg" {
  name     = "rg-ai-high-severity"
  location = "Central India"
}

resource "azurerm_storage_account" "high_severity_sa" {
  name                     = "aihighseverity123"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  # 🚨 HIGH (new attribute name)
  allow_nested_items_to_be_public = true

  # 🚨 MEDIUM
  min_tls_version = "TLS1_0"

  # 🚨 MEDIUM (new attribute name)
  https_traffic_only_enabled = false
}