# HL7 SIU Parser for Appointments

## Overview

This parser reads HL7 SIU^S12 messages from a `.hl7` file, extracts appointment data from key segments (`MSH`, `SCH`, `PID`, `PV1`), validates it, and outputs structured JSON.

---

## Features

- Parses multiple HL7 messages per file
- Manual parsing (no external HL7 libraries)
- Field-level validation (required fields present & non-empty)
- Schema validation (correct types and structure)
- Unit tested
- CLI and Docker support

---

## Requirements

- Python 3.8+
- Docker
- No external dependencies

---

## Usage

### Run with Python

```bash
python main.py input.hl7
```

### Run with Docker

```bash
# Build the image
docker build -t hl7_parser .

# Run the parser
docker run --rm -v "$PWD:/app" hl7_parser input.hl7
```

---

## Output

Example JSON:

```json
{
  "appointment_id": "123456",
  "appointment_datetime": "2025-05-02T13:00:00Z",
  "patient": {
    "id": "P12345",
    "first_name": "John",
    "last_name": "Doe",
    "dob": "1985-02-10",
    "gender": "M"
  },
  "provider": {
    "id": "D67890",
    "name": "Dr. Smith"
  },
  "location": "Clinic A - Room 203",
  "reason": "General Consultation"
}
```

---

## Validation

- `validate_json_data`: Ensures required fields are present and non-empty
- `validate_json_schema`: Ensures structure and type correctness

Invalid messages are skipped with printed errors.

---

## Tests

Run unit tests using:

```bash
python -m unittest unit_test.py
```

---

## File Structure

```
├── main.py               # Entry point, CLI logic
├── parser.py             # HL7 parsing logic
├── validate_data.py      # Field-level validator
├── validate_schema.py    # JSON Schema validator
├── unit_test.py          # Unit test
├── input.hl7             # Sample input file
├── Dockerfile            # Docker support
```

---
