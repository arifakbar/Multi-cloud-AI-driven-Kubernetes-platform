import json

def extract_summary(plan_path: str):
    with open(plan_path) as f:
        plan = json.load(f)

    summary = {
        "creates": [],
        "updates": [],
        "deletes": []
    }

    for rc in plan.get("resource_changes", []):
        actions = rc.get("change", {}).get("actions", [])
        resource_data = {
            "type": rc.get("type"),
            "name": rc.get("name"),
            "after": rc.get("change", {}).get("after", {})
        }

        if "create" in actions:
            summary["creates"].append(resource_data)
        elif "update" in actions:
            summary["updates"].append(resource_data)
        elif "delete" in actions:
            summary["deletes"].append(resource_data)

    return summary