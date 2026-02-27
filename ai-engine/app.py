import json
import sys
from terraform_analyzer import extract_summary
from llm_client import call_llm_json

def analyze(plan_path: str):
    summary = extract_summary(plan_path)

    with open("ai-engine/prompts/terraform_review.txt") as f:
        template = f.read()

    prompt = template.replace(
        "{{SUMMARY}}",
        json.dumps(summary, indent=2)
    )

    result = call_llm_json(prompt)

    return result


if __name__ == "__main__":
    plan_file = sys.argv[1] if len(sys.argv) > 1 else "plan.json"

    report = analyze(plan_file)

    print(json.dumps(report, indent=2))

    if report["risk_level"] == "high":
        raise SystemExit("High risk detected. Failing pipeline.")