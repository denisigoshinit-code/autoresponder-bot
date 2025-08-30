# server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import os

def run_http_server():
    port = int(os.getenv("PORT", 10000))  # Render сам задаёт PORT
    server = HTTPServer(('', port), lambda *args, **kwargs: BaseHTTPRequestHandler(*args, **kwargs))
    
    def handler(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is alive (polling mode)")

    server.RequestHandlerClass.do_GET = handler
    print(f"🔧 Health server запущен на порту {port}")
    server.serve_forever()

# Запускаем в отдельном потоке
threading.Thread(target=run_http_server, daemon=True).start()