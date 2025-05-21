import json
import os
from urllib.parse import parse_qs

def handler(request):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET"
    }

    query = parse_qs(request.query_string.decode())
    names = query.get("name", [])

    # Load marks.json relative to this file's directory
    path = os.path.join(os.path.dirname(__file__), '..', 'marks.json')
    with open(path, 'r') as f:
        data = json.load(f)

    # Convert list of dicts into a lookup dict {name: marks}
    marks_data = {student['name']: student['marks'] for student in data}

    result = [marks_data.get(name) for name in names]

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps({"marks": result})
    }
