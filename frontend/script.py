import http.server
import socketserver

PORT = 3000

print("🌟 Starting LinguaSpark Frontend...")
print(f"💻 Open your browser at: http://localhost:{PORT}")
print("Press Ctrl+C to stop the server")

Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()