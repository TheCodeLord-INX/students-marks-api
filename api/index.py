import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Enable CORS for all origins
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Parse the URL and query parameters
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # Load student marks data
        try:
            # Get the directory of the current file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one level to the root directory
            root_dir = os.path.dirname(current_dir)
            json_path = os.path.join(root_dir, 'q-vercel-python.json')
            
            with open(json_path, 'r') as f:
                student_data = json.load(f)
            
            # Convert array of objects to dictionary for faster lookup
            student_marks = {student['name']: student['marks'] for student in student_data}
            
        except FileNotFoundError:
            # Fallback: return empty response if file not found
            student_marks = {}
        
        # Get the 'name' parameters from the query
        names = query_params.get('name', [])
        
        # Get marks for each name in the same order
        marks = []
        for name in names:
            if name in student_marks:
                marks.append(student_marks[name])
            else:
                marks.append(None)  # or you could skip missing names
        
        # Return JSON response
        response = {"marks": marks}
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def do_OPTIONS(self):
        # Handle preflight requests for CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()