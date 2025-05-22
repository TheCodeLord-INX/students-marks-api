from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            # Student data embedded directly
            student_data = [
                {"name":"LABw8Sr","marks":67},{"name":"hLVcf0D","marks":90},{"name":"3","marks":24},{"name":"DEj17Av2","marks":1},{"name":"B3J6knfIp","marks":98},{"name":"kkflB6a","marks":74},{"name":"gbp0R4","marks":80},{"name":"NgQ","marks":37},{"name":"q3n6gCX4i","marks":93},{"name":"9rj","marks":16},{"name":"rwSW","marks":23},{"name":"fXqI","marks":96},{"name":"IflSpgGRs","marks":79},{"name":"R5ydyS","marks":90},{"name":"lHLbY","marks":87},{"name":"o2","marks":70},{"name":"7","marks":82},{"name":"S4bKSKdT","marks":67},{"name":"g8kKJb","marks":94},{"name":"0d2s","marks":30},{"name":"xJe7TO","marks":94},{"name":"brz","marks":81},{"name":"5","marks":1},{"name":"wlzLDSmFnb","marks":74},{"name":"UpR","marks":22},{"name":"kDmNNdle1","marks":90},{"name":"2z0ZcTNwo","marks":30},{"name":"eaaww6x","marks":59},{"name":"Y5gYbjkg6","marks":92},{"name":"z4Nmfdnf4z","marks":14},{"name":"Y0AdYqAN","marks":66},{"name":"7GRpP","marks":93},{"name":"d6ph","marks":79},{"name":"5MOaJL","marks":12},{"name":"jh2M","marks":33},{"name":"hTlF1ZWAL","marks":11},{"name":"0Y","marks":6},{"name":"X960","marks":67},{"name":"CUQ","marks":93},{"name":"aXhcxyWu","marks":60},{"name":"uL7","marks":71},{"name":"plx","marks":23},{"name":"g","marks":67},{"name":"C","marks":0},{"name":"sZ8qElPUD1","marks":49},{"name":"a56dx9VYl","marks":94},{"name":"hxyiIJj","marks":65},{"name":"FWh","marks":18},{"name":"i3","marks":97},{"name":"2jlr7","marks":94},{"name":"lw","marks":60},{"name":"7XFPCrHf","marks":34},{"name":"EMC9VmXQp","marks":6},{"name":"be2G8pt","marks":98},{"name":"IR9C","marks":57},{"name":"2Ui4","marks":38},{"name":"fOW","marks":36},{"name":"uq5","marks":16},{"name":"Ju","marks":73},{"name":"9tglrs4Mcx","marks":10},{"name":"rOPZn9xF","marks":99},{"name":"zxRfVy","marks":29},{"name":"LGg","marks":1},{"name":"T2oHCO66Q","marks":42},{"name":"mdly","marks":6},{"name":"oDpVsJ","marks":77},{"name":"i","marks":56},{"name":"Bnh1ia","marks":36},{"name":"0T","marks":9},{"name":"HHkqV7EJM","marks":83},{"name":"OoZsApttfk","marks":74},{"name":"8NXF9z","marks":0},{"name":"m7Dw3rS6Eh","marks":51},{"name":"7APDQ","marks":41},{"name":"GAI7f","marks":27},{"name":"UmoO","marks":60},{"name":"hDaaFts","marks":54},{"name":"jX454pgnPI","marks":73},{"name":"Ke0TnGS","marks":93},{"name":"JvW","marks":15},{"name":"Y2Rig","marks":16},{"name":"UOlQ5sGWa4","marks":64},{"name":"W","marks":54},{"name":"TIOSk","marks":28},{"name":"UWiOvdmJ","marks":15},{"name":"ByCjeBlNRQ","marks":37},{"name":"4","marks":75},{"name":"NqZoj3","marks":24},{"name":"LE2KL8oXT","marks":21},{"name":"f3m","marks":93},{"name":"DD","marks":27},{"name":"6UxQ","marks":85},{"name":"3mNygR0k","marks":19},{"name":"6U7Xw","marks":29},{"name":"Wru2x1zO","marks":9},{"name":"sRfYTVod","marks":70},{"name":"FfOFShROZL","marks":80},{"name":"I0XYlkR","marks":48},{"name":"dPO5ZR","marks":41},{"name":"aQ","marks":49}
            ]
            
            # Convert to dictionary for fast lookup
            student_marks = {student['name']: student['marks'] for student in student_data}
            
            # Parse URL and get query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            # Get the 'name' parameters
            names = query_params.get('name', [])
            
            # If no names provided, return usage info
            if not names:
                response = {
                    "message": "Provide student names using ?name=studentName",
                    "example": "?name=LABw8Sr&name=hLVcf0D", 
                    "sample_names": ["LABw8Sr", "hLVcf0D", "3", "DEj17Av2", "B3J6knfIp"],
                    "marks": []
                }
            else:
                # Get marks for requested names in order
                marks = []
                for name in names:
                    if name in student_marks:
                        marks.append(student_marks[name])
                    else:
                        marks.append(None)
                
                response = {"marks": marks}
            
            # Send JSON response
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            # Handle any errors
            error_response = {
                "error": f"Server error: {str(e)}",
                "marks": []
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()