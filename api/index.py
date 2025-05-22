import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
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
            student_marks = {}
            try:
                # Try multiple possible paths for the JSON file
                possible_paths = [
                    'q-vercel-python.json',
                    './q-vercel-python.json',
                    '../q-vercel-python.json',
                    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'q-vercel-python.json')
                ]
                
                student_data = None
                for path in possible_paths:
                    try:
                        with open(path, 'r') as f:
                            student_data = json.load(f)
                        break
                    except (FileNotFoundError, IOError):
                        continue
                
                if student_data is None:
                    # If file not found, return error response
                    response = {
                        "error": "Student data file not found",
                        "marks": []
                    }
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                    return
                
                # Convert array of objects to dictionary for faster lookup
                if isinstance(student_data, list):
                    student_marks = {student['name']: student['marks'] for student in student_data}
                else:
                    student_marks = student_data
                    
            except json.JSONDecodeError as e:
                response = {
                    "error": f"JSON decode error: {str(e)}",
                    "marks": []
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            except Exception as e:
                response = {
                    "error": f"Error loading data: {str(e)}",
                    "marks": []
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            # Get the 'name' parameters from the query
            names = query_params.get('name', [])
            
            if not names:
                # If no names provided, return all available names (for debugging)
                response = {
                    "available_names": list(student_marks.keys())[:10],  # First 10 names
                    "total_students": len(student_marks),
                    "marks": []
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            # Get marks for each name in the same order
            marks = []
            for name in names:
                if name in student_marks:
                    marks.append(student_marks[name])
                else:
                    marks.append(None)  # Return null for missing names
            
            # Return JSON response
            response = {"marks": marks}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            # Catch any other errors
            try:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {
                    "error": f"Server error: {str(e)}",
                    "marks": []
                }
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
            except:
                pass  # If we can't even send an error response, just fail silently
    
    def do_OPTIONS(self):
        # Handle preflight requests for CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()