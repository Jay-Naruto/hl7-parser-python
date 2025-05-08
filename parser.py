from datetime import datetime
from validate_data import validate_json_data

def parse_hl7_message(hl7_message: str) -> dict:
    json_structure = {
        "appointment_id": "",
        "appointment_datetime": "",
        "patient": {
            "id": "",
            "first_name": "",
            "last_name": "",
            "dob": "",
            "gender": ""
        },
        "provider": {
            "id": "",
            "name": ""
        },
        "location": "",
        "reason": ""
    }

    sections = hl7_message.strip().splitlines()

    required_sections = {"MSH","SCH", "PID", "PV1"}
    present = {line.split('|')[0].strip() for line in sections if line.strip()}
    missing = required_sections - present

    if missing:
        print(f"Malformed message: Missing required sections: {', '.join(missing)}")
        return None     
    

    for section in sections:
        section = section.strip()
        fields = section.split('|')

        if not fields:
            continue


        if fields[0] =="SCH":

            if len(fields) > 1:
                json_structure["appointment_id"] = fields[1].split('^')[0]
            if len(fields) > 3 and fields[3]:
                try:
                    dt = datetime.strptime(fields[3][:12], "%Y%m%d%H%M")
                    json_structure["appointment_datetime"] = dt.isoformat() + "Z"
                except ValueError:
                    print(f"Inappropriate Date Format")
                    pass
            if len(fields) > 5:
                json_structure["location"] = fields[5].strip()
            if len(fields) > 2:
                json_structure["reason"] = fields[2].strip()

        elif fields[0] =="PID":

            if len(fields) > 3:
                json_structure["patient"]["id"] = fields[3].split('^')[0]
            if len(fields) > 5:
                name_parts = fields[5].split('^')
                if len(name_parts) > 0:
                    json_structure["patient"]["last_name"] = name_parts[0]
                if len(name_parts) > 1:
                    json_structure["patient"]["first_name"] = name_parts[1]

            if len(fields) > 7:
                dob = fields[7].strip()
                if len(dob) != 8 or not dob.isdigit():
                    print("Inappropriate DOB format: must be 8 digits YYYYMMDD")
                else:
                    try:
                        dt = datetime.strptime(dob, "%Y%m%d")
                        json_structure["patient"]["dob"] = dt.strftime("%Y-%m-%d")
                    except ValueError:
                        print("Inappropriate DOB value: invalid calendar date")


            if len(fields) > 8:
                json_structure["patient"]["gender"] = fields[8]

        elif fields[0] =="PV1":

            if len(fields) > 3:
                provider = fields[3].split('^')
                json_structure["provider"]["id"] = provider[0]
                if len(provider) > 2:
                    json_structure["provider"]["name"] =f"{provider[2]}. {provider[1]}"
                elif len(provider) > 1:
                    json_structure["provider"]["name"] = provider[1]
    try:
            validate_json_data(json_structure)
    except ValueError as e:
            print(f"Validation error: {e}")
            return None

    return json_structure

 # type: ignore