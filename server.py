# server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import os

def run_http_server():
    # ✅ Берём порт из переменной окружения
    port = int(os.getenv("PORT", 10000))

    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Bot is alive (polling mode)")

    try:
        # ✅ Привязываемся к 0.0.0.0 и динамическому порту
        server = HTTPServer(('0.0.0.0', port), HealthHandler)
        print(f"🔧 Health server запущен на http://0.0.0.0:{port}")
        server.serve_forever()
    except OSError as e:
        if e.errno == 98:
            print(f"❌ Порт {port} уже занят. Попробуйте перезапустить сервис.")
        else:
            raise

# Запускаем в отдельном потоке
threading.Thread(target=run_http_server, daemon=True).start()