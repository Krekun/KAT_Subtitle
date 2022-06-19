import http.server
import socketserver
import webbrowser
import os

#Lunch Server
#Without server, you need to aloow browser to use your microphone every time.

class localserver():
    def __init__(self) -> None:
        PORT = 8002
        Handler = http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            # print("serving at port", PORT)
            url="http://localhost:8002/"
            webbrowser.open(url)
            # os.system("taskkill /im chrome.exe /f")
            # print("サーバー起動")
            httpd.serve_forever()

if __name__=="__main__":
    localserver()