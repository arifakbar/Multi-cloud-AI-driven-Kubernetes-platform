import json
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
    report = analyze("plan.json")
    print(json.dumps(report, indent=2))

    # Governance rule
    if report["risk_level"] == "high":
        raise SystemExit("High risk detected. Failing pipeline.")