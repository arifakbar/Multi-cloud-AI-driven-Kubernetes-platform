from base import build_violation, ensure_list


def check(resource):
    if resource.get("type") != "azurerm_storage_account":
        return None

    after = resource.get("change", {}).get("after", {})
    violations = []

    if after.get("allow_blob_public_access") is True:
        violations.append(
            build_violation("high", "Azure Storage Account allows public blob access")
        )

    if after.get("min_tls_version") != "TLS1_2":
        violations.append(
            build_violation("medium", "Storage account does not enforce TLS 1.2")
        )

    if after.get("enable_https_traffic_only") is False:
        violations.append(
            build_violation("medium", "HTTPS traffic is not enforced")
        )

    return ensure_list(violations)