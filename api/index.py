import json
import os
from urllib.parse import parse_qs

def app(request, response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET"

    query = parse_qs(request.query_string.decode())
    names = query.get("name", [])

    path = os.path.join(os.path.dirname(__file__), '..', 'marks.json')
    with open(path, 'r') as f:
        marks_data = json.load(f)

    result = [marks_data.get(name, None) for name in names]
    return response.json({ "marks": result })
