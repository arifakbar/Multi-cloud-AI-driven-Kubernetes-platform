import json
import sys

with open("violations.json") as f:
    data = json.load(f)

high_found = any(v["severity"].lower() == "high" for v in data.get("violations", []))

if high_found:
    print("HIGH severity violations found.")
    sys.exit(2)  # special exit code
else:
    print("No HIGH severity violations.")
    sys.exit(0)