

def validate_json_schema(json_data: dict, schema:dict, parent ="") -> list:
    all_errors=[]
    
    for key, value in schema.items():
        new_key = f"{parent}.{key}" if parent else key
        if key not in json_data:
            all_errors.append(f"Missing key: {new_key}")
            continue

        if isinstance(value, dict):
            if not isinstance(json_data[key], dict):
                all_errors.append(f"Expected object for key: {new_key}")
            else:
                nested_errors = validate_json_schema(json_data[key], value, new_key)
                all_errors.extend(nested_errors)
        else: 
            if not isinstance(json_data[key], value):
                all_errors.append(f"Key '{new_key}' should be of type {value.__name__}, got {type(json_data[key]).__name__}")
    return all_errors
