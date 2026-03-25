import json
import threading
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

class DataStore:
    latest_data = {"detections": []}

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            # Disable caching
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.end_headers()
            self.wfile.write(json.dumps(DataStore.latest_data).encode('utf-8'))
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Vision - Live Stream</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #09090b;
            --surface: rgba(255, 255, 255, 0.03);
            --border: rgba(255, 255, 255, 0.1);
            --accent: #22d3ee;
            --text-glow: 0 0 10px rgba(34, 211, 238, 0.5);
        }
        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg);
            color: #f8fafc;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }
        h1 {
            font-weight: 300;
            letter-spacing: 2px;
            margin-bottom: 5px;
            text-transform: uppercase;
        }
        .status {
            color: #10b981;
            font-size: 0.9rem;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .pulse {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 10px #10b981;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }
        .container {
            width: 100%;
            max-width: 500px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .card {
            background: var(--surface);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            border-color: rgba(255,255,255,0.2);
        }
        .tool-info {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .tool-name {
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--accent);
            text-shadow: var(--text-glow);
            text-transform: capitalize;
            margin-bottom: 2px;
        }
        .tool-bbox {
            font-family: monospace;
            color: #94a3b8;
            font-size: 0.85rem;
            background: rgba(0,0,0,0.3);
            padding: 4px 8px;
            border-radius: 6px;
        }
        .confidence-circle {
            position: relative;
            width: 60px;
            height: 60px;
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 50%;
            background: conic-gradient(var(--accent) var(--progress), #1e293b 0deg);
        }
        .confidence-inner {
            width: 50px;
            height: 50px;
            background: var(--bg);
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: 700;
            font-size: 0.9rem;
        }
        .empty-state {
            text-align: center;
            color: #64748b;
            padding: 40px 20px;
            border: 1px dashed #334155;
            border-radius: 16px;
        }
    </style>
</head>
<body>
    <h1>Vision Feed</h1>
    <div class="status"><div class="pulse"></div> Live Inference Data</div>
    <div class="container" id="feed">
        <div class="empty-state">Awaiting connection...</div>
    </div>

    <script>
        async function fetchDetections() {
            try {
                const response = await fetch('/data');
                const data = await response.json();
                const feed = document.getElementById('feed');
                
                if (!data.detections || data.detections.length === 0) {
                    feed.innerHTML = '<div class="empty-state">No tools in frame</div>';
                    return;
                }

                feed.innerHTML = data.detections.map(d => {
                    const confPercent = Math.round(d.confidence * 100);
                    return `
                        <div class="card">
                            <div class="tool-info">
                                <span class="tool-name">${d.class}</span>
                                <span class="tool-bbox">L: ${d.bbox[0]}, T: ${d.bbox[1]}, R: ${d.bbox[2]}, B: ${d.bbox[3]}</span>
                            </div>
                            <div class="confidence-circle" style="--progress: ${confPercent * 3.6}deg">
                                <div class="confidence-inner">${confPercent}%</div>
                            </div>
                        </div>
                    `;
                }).join('');
            } catch (err) {
                console.error(err);
            }
        }
        // Fetch 5 times a second
        setInterval(fetchDetections, 200);
    </script>
</body>
</html>
"""
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress logging to keep YOLO console clear
        pass

class HTTPSender:
    def __init__(self, port=8080):
        self.port = port
        self.server = HTTPServer(('0.0.0.0', port), RequestHandler)

    def start(self):
        thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        thread.start()
        
        # Get local IP dynamically
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
            
        print("\\n" + "="*50)
        print("🌐 HTTP LIVE STREAM READY")
        print(f"👉 Open your phone browser to: http://{ip}:{self.port}")
        print("="*50 + "\\n")

    def send_data(self, data_dict):
        # Update the latest frame data
        DataStore.latest_data = data_dict

    def close(self):
        self.server.shutdown()
        self.server.server_close()
