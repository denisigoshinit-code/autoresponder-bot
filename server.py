# server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import os

def run_http_server():
    port = int(os.getenv("PORT", 10000))
    
    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Bot is alive (polling mode)")

    # ✅ Ключевое исправление: host='0.0.0.0'
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    print(f"🔧 Health server запущен на http://0.0.0.0:{port}")
    server.serve_forever()

# Запускаем в отдельном потоке
threading.Thread(target=run_http_server, daemon=True).start()