provider "azurerm" {
  # AzureRM provider 2.x
  version = "~> 4.0"
  # v2.x required "features" block
  features {}
}

# Create an Azure IoT Hub
resource "azurerm_iothub" "iothub" {
    name                = "mlops-iothub"
    resource_group_name = "${var.resource_prefix}"
    location = "${var.location}"

    sku {
        name     = "F1"
        capacity = 1
    }
}

# Create an IoT Hub Access Policy
# data "azurerm_iothub_shared_access_policy" "iothub" {
#     name                = "iothubowner"
#     resource_group_name = azurerm_resource_group.iothub.name
#     iothub_name         = azurerm_iothub.iothub.name
# }

# # Create a Device Provisioning Service
# resource "azurerm_iothub_dps" "iothubdps" {
#     name                = "mlops-dps"
#     resource_group_name = azurerm_resource_group.iothub.name
#     location            = azurerm_resource_group.iothub.location

#     sku {
#         name     = "S1"
#         capacity = 1
#     }

#     linked_hub {
#         connection_string = data.azurerm_iothub_shared_access_policy.iothub.primary_connection_string
#         location          = azurerm_resource_group.iothub.location
#     }
# }