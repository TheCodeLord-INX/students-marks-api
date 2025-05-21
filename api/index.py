import json
import os
from urllib.parse import parse_qs

def app(request, response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET"

    query = parse_qs(request.query_string.decode())
    names = query.get("name", [])

    with open(os.path.join(os.path.dirname(__file__), '..', 'marks.json')) as f:
        marks_data = json.load(f)

    result = [marks_data.get(name, None) for name in names]
    response.status_code = 200
    return response.json({"marks": result})
