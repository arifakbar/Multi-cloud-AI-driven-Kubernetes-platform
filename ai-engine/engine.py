from rules.aws import s3
from rules.azure import storage_account

def evaluate_resource(resource):
    resource_type = resource.get("type")

    # AWS Routing
    if resource_type == "aws_s3_bucket":
        return s3.check(resource)

    # Azure Routing
    if resource_type == "azurerm_storage_account":
        return storage_account.check(resource)

    return []