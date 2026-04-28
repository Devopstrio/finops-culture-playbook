provider "azurerm" {
  features {}
}

# --- FinOps Foundation (Institutional Hub) ---

resource "azurerm_resource_group" "finops" {
  name     = "rg-${var.project_name}-foundation-${var.environment}"
  location = var.location
}

# --- Analytics Storage (Postgres) ---

resource "azurerm_postgresql_flexible_server" "finops" {
  name                   = "psql-${var.project_name}-spend-${var.environment}"
  resource_group_name    = azurerm_resource_group.finops.name
  location               = azurerm_resource_group.finops.location
  version                = "13"
  administrator_login    = "finopsadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2ds_v4"
}

# --- Spend Metadata Store (Storage Account) ---

resource "azurerm_storage_account" "spend_data" {
  name                     = "stfinopsspend${var.environment}"
  resource_group_name      = azurerm_resource_group.finops.name
  location                 = azurerm_resource_group.finops.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    Environment = var.environment
    CostCenter  = "FinOps-Hub"
  }
}

# --- Monitoring & Observability (Log Analytics) ---

resource "azurerm_log_analytics_workspace" "finops" {
  name                = "log-${var.project_name}-insights-${var.environment}"
  location            = azurerm_resource_group.finops.location
  resource_group_name = azurerm_resource_group.finops.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

# --- Container Apps Environment (Runtime) ---

resource "azurerm_container_app_environment" "finops" {
  name                       = "cae-${var.project_name}-${var.environment}"
  location                   = azurerm_resource_group.finops.location
  resource_group_name        = azurerm_resource_group.finops.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.finops.id
}
