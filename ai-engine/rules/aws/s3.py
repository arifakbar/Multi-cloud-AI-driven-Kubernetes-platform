from base import build_violation, ensure_list


def check(resource):
    if resource.get("type") != "aws_s3_bucket":
        return None

    after = resource.get("change", {}).get("after", {})
    violations = []

    if after.get("acl") in ["public-read", "public-read-write"]:
        violations.append(
            build_violation("high", "S3 bucket has public ACL configured")
        )

    if after.get("policy"):
        violations.append(
            build_violation("medium", "S3 bucket has a policy attached. Ensure it is not public.")
        )

    versioning = after.get("versioning", {})
    if isinstance(versioning, dict) and not versioning.get("enabled", False):
        violations.append(
            build_violation("low", "S3 bucket versioning is not enabled")
        )

    return ensure_list(violations)