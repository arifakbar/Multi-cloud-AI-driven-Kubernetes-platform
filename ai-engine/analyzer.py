import json
import sys
import traceback
from engine import analyze_plan

from rag_retriever import RAGRetriever
from llm_generator import LLMGenerator


def enrich_with_ai(violations):
    """
    Adds RAG retrieval + LLM explanation to each violation.
    Fails gracefully if AI components break.
    """
    try:
        retriever = RAGRetriever()
        generator = LLMGenerator()
    except Exception as e:
        print(f"⚠️ AI components failed to initialize: {e}")
        return violations

    enriched = []

    for v in violations:
        try:
            issue_text = v.get("issue") or v.get("message") or "security violation"

            query = (
                f"{issue_text} {v.get('resource', '')} "
                f"CIS compliance risk impact remediation"
            )

            rag_context = retriever.search(query)
            
            explanation = generator.generate_explanation(
                violation={
                    "resource": v.get("resource"),
                    "issue": issue_text,
                    "severity": v.get("severity")
                },
                rag_context=rag_context
            )

            v["rag_context"] = rag_context
            v["ai_explanation"] = explanation

        except Exception as e:
            print(f"⚠️ AI enrichment failed for {v.get('resource')}: {e}")
            v["ai_explanation"] = "AI explanation unavailable."

        enriched.append(v)

    return enriched


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

    print("Running deterministic rule engine...")
    violations = analyze_plan(plan)

    if violations:
        print("Enhancing violations with RAG + LLM...")
        violations = enrich_with_ai(violations)
    else:
        print("No violations found. Skipping AI enrichment.")

    # Normalize severity case
    for v in violations:
        v["severity"] = v["severity"].lower()

    high_count = sum(1 for v in violations if v["severity"] == "high")
    medium_count = sum(1 for v in violations if v["severity"] == "medium")
    low_count = sum(1 for v in violations if v["severity"] == "low")

    output = {
        "total_violations": len(violations),
        "high": high_count,
        "medium": medium_count,
        "low": low_count,
        "violations": violations
    }

    # Write structured output
    with open("violations.json", "w") as f:
        json.dump(output, f, indent=2)

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()