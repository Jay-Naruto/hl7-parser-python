def validate_json_data(json_data: dict):
    missing = []

    if not json_data.get("appointment_id"):
        missing.append("Appointment ID")
    if not json_data.get("appointment_datetime"):
        missing.append("Appointment datetime")
    if not json_data.get("location"):
        missing.append("Location")
    if not json_data.get("reason"):
        missing.append("Reason")

    patient = json_data.get("patient", {})
    if not patient.get("id"):
        missing.append("Patient ID")
    if not patient.get("first_name"):
        missing.append("Patient First Name")
    if not patient.get("last_name"):
        missing.append("Patient Last Name")
    if not patient.get("dob"):
        missing.append("Patient DOB")
    if not patient.get("gender"):
        missing.append("Patient Gender")

    provider = json_data.get("provider", {})
    if not provider.get("id"):
        missing.append("Provider ID")
    if not provider.get("name"):
        missing.append("Provider Name")

    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
