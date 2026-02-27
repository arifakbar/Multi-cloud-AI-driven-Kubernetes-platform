from rules.base import Violation

def check(resource):
    violations = []

    after = resource.get("change", {}).get("after", {})
    address = resource.get("address")

    if after.get("allow_blob_public_access") is True:
        violations.append(Violation(
            address,
            "AZURE_BLOB_PUBLIC_ACCESS",
            "high",
            "Azure Storage allows public blob access."
        ))

    if after.get("min_tls_version") != "TLS1_2":
        violations.append(Violation(
            address,
            "AZURE_TLS_NOT_1_2",
            "high",
            "Storage account must enforce TLS1_2."
        ))

    if after.get("enable_https_traffic_only") is not True:
        violations.append(Violation(
            address,
            "AZURE_HTTPS_ONLY_DISABLED",
            "high",
            "HTTPS-only must be enabled."
        ))

    return violations