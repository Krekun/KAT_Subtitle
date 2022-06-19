import http.server
import socketserver


class localserver():
    def __init__(self) -> None:
        PORT = 8001
        Handler = http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("serving at port", PORT)
            httpd.serve_forever()

if __name__=="__main__":
    localserver()