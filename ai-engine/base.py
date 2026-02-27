# ai-engine/base.py

def build_violation(severity: str, message: str):
    return {
        "severity": severity,
        "message": message
    }


def ensure_list(result):
    """
    Ensures rule returns list or None
    """
    if not result:
        return None

    if isinstance(result, list):
        return result

    return [result]