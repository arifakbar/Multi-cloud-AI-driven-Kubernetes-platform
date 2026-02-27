import json
import sys


def main():
    try:
        with open("violations.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to read violations.json: {e}")
        sys.exit(1)

    high_count = data.get("high", 0)

    print(f"High severity violations: {high_count}")

    if high_count > 0:
        print("high=true")
        sys.exit(1)

    print("high=false")
    sys.exit(0)


if __name__ == "__main__":
    main()