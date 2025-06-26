# validators.py

def validate_rate_input(data, require_all_fields=True):
    """
    Validates the input for a bank rate.
    
    Parameters:
        data (dict): The input JSON from the user
        require_all_fields (bool): Whether to enforce all fields being present (POST = True, PUT = False)

    Returns:
        (bool, dict or str): (True, cleaned_data) if valid, (False, error_message) if invalid
    """

    # Define the required fields in our JSON structure so our validator knows what to look for. 
    required_fields = ["bank", "country", "account_type", "interest_rate", "compounding"]
    cleaned = {}

    # Check that all required fields are present in the incoming data. 
    if require_all_fields:
        missing = [f for f in required_fields if f not in data]
        if missing:
            return False, f"Missing fields: {', '.join(missing)}"

    # Iterate over the fields pulling the "value" from the input and comparing it to the "field" of our JSON structure. 
    for field in required_fields: # Loop over the expected fields. (country, bank, interest_rate)
        if field in data: # Only proceed if the field was included in the incoming data
            value = data[field] # Grab the user-provided data for the field 
            if isinstance(value, str) and not value.strip(): # strip() remove leading and trailing white spaces and then will check if the field was empty after that operation. 
                return False, f"Field '{field}' cannot be empty"
            # Check that interest rate is a postive integer or floating integer
            if field == "interest_rate":
                try: # Try turning the value to a float. 2.5 -> 2 will work. "Hello" will not convert and error out
                    value = float(value) 
                    if value < 0:
                        return False, "interest_rate must be a positive number"
                    cleaned[field] = value # Store the float as our sanitized value
                except ValueError:
                    return False, "interest_rate must be a number"
            else:
                cleaned[field] = value.strip() if isinstance(value, str) else value

    # Return the True boolean and our sanitized data
    return True, cleaned