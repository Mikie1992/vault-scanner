from fastapi import FastAPI, Request, Form, Response
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import telemetry
import sqlite3

# Initialize templates and app
template = Environment(loader=FileSystemLoader('./templates'))
app = FastAPI()

def find_vulnerabilities(code):
    vulnerabilities = []
    if 'sk-' in code: vulnerabilities.append('OpenAI Key Exposed')
    if 'AKIA' in code: vulnerabilities.append('AWS Key Exposed')
    if 'mongodb://' in code: vulnerabilities.append('MongoDB Connection String Hardcoded')
    return vulnerabilities

@app.get('/')
def index(request: Request):
    html = template.get_template('index.html').render()
    return Response(content=html, media_type="text/html")

@app.post('/scan')
def scan(code: str = Form(...)):
    vulnerabilities = find_vulnerabilities(code)
    
    # Telemetry Integration
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for vuln in vulnerabilities:
        try:
            telemetry.log_scan_metadata(vuln, 'Python', timestamp)
        except Exception as e:
            print(f"Telemetry engine error: {e}")

    if vulnerabilities:
        html = template.get_template('results.html').render(vulnerabilities=vulnerabilities)
    else:
        html = template.get_template('results.html').render(vulnerabilities=['No vulnerabilities found! Code is secure.'])
    return Response(content=html, media_type="text/html")

# --- THE NEW ADMIN DASHBOARD ROUTE ---
@app.get('/admin')
def admin_dashboard(request: Request):
    try:
        conn = sqlite3.connect('telemetry.sqlite')
        cursor = conn.cursor()
        # Fetch all rows, newest first
        cursor.execute("SELECT id, vulnerability_type, language, timestamp FROM scan_log ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
    except Exception as e:
        rows = []
        print(f"Database error: {e}")
        
    html = template.get_template('admin.html').render(rows=rows)
    return Response(content=html, media_type="text/html")

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)