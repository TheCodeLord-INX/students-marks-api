import json
import os
from urllib.parse import parse_qs

def handler(request, response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET"

    query = parse_qs(request.query_string.decode())
    names = query.get("name", [])

    path = os.path.join(os.path.dirname(__file__), '..', 'marks.json')
    with open(path, 'r') as f:
        marks_data = json.load(f)

    result = [marks_data.get(name, None) for name in names]
    response.status_code = 200
    response.body = json.dumps({"marks": result})
