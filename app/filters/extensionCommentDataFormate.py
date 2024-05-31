import json

# Extract the JSON string and parse it into a Python dictionary
def serialiseTextIntoJson(data):
    # Extract the JSON string from the "message" key and remove the surrounding triple backticks
    message = data["message"].strip("```json\n```")

    # Parse the JSON string into a Python dictionary
    try:
        parsed_data = json.loads(message)
        return parsed_data  # Return the parsed dictionary
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return None  # Return None if JSON decoding fails
