import json
import sys
from engine import analyze_plan


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <plan.json>")
        sys.exit(1)

    plan_path = sys.argv[1]

    try:
        with open(plan_path, "r") as f:
            plan = json.load(f)
    except Exception as e:
        print(f"Failed to load plan file: {e}")
        sys.exit(1)

    # Run deterministic rule engine
    violations = analyze_plan(plan)

    output = {
        "total_violations": len(violations),
        "high": sum(1 for v in violations if v["severity"] == "high"),
        "medium": sum(1 for v in violations if v["severity"] == "medium"),
        "low": sum(1 for v in violations if v["severity"] == "low"),
        "violations": violations
    }

    # Write structured output file
    with open("violations.json", "w") as f:
        json.dump(output, f, indent=2)

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()