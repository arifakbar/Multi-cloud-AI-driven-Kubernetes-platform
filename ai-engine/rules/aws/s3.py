from rules.base import Violation

def check(resource):
    violations = []

    after = resource.get("change", {}).get("after", {})
    address = resource.get("address")

    # Public ACL
    if after.get("acl") in ["public-read", "public-read-write"]:
        violations.append(Violation(
            address,
            "S3_PUBLIC_ACL",
            "high",
            "S3 bucket has public ACL."
        ))

    # Versioning
    if not after.get("versioning", {}).get("enabled", False):
        violations.append(Violation(
            address,
            "S3_VERSIONING_DISABLED",
            "medium",
            "S3 bucket versioning is disabled."
        ))

    return violations