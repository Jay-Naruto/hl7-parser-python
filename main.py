import sys
from parser import parse_hl7_message # type: ignore
from validate_schema import validate_json_schema # type: ignore
import json


schema = {
    "appointment_id": str,
    "appointment_datetime": str,
    "patient": {
        "id": str,
        "first_name": str,
        "last_name": str,
        "dob": str,
        "gender": str
    },
    "provider": {
        "id": str,
        "name": str
    },
    "location": str,
    "reason": str
}

def split_messages(file: str) -> list:
    lines =file.strip().splitlines()
    messages =[]
    current= []
    for line in lines:
        if line.startswith("MSH|") and current:
             messages.append('\n'.join(current))
             current = [line]
        else:
             current.append(line)
    if current:
        messages.append('\n'.join(current))
    return messages


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <hl7_file>")
        sys.exit(1)
    with open(sys.argv[1], 'r') as file:
        hl7_message = file.read()

    messages = split_messages(hl7_message)
    results = []
    for msg in messages:
        parsed = parse_hl7_message(msg)
        if parsed:
            results.append(parsed)

    all_errors =[]
    for parsed_data in results:
        all_errors.extend(validate_json_schema(parsed_data, schema))

    if all_errors:
        print("JSON Schema validation errors:")
        for err in all_errors:
            print("-", err)
    else:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()