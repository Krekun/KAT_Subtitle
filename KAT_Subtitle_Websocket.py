import threading
import http.server
import socketserver
import webbrowser

from websocket_server import WebsocketServer


class Websocket:
    def __init__(self, queue=None) -> None:
        self.q_sentence = queue
        websocket_thread = threading.Thread(target=self.websocket)
        server_thread = threading.Thread(target=self.server)
        websocket_thread.start()
        server_thread.start()

    def websocket(self):
        server = WebsocketServer(port=5001, host="127.0.0.1")
        server.set_fn_new_client(self.new_client)
        server.set_fn_message_received(self.message_received)
        server.run_forever()

    def new_client(self, client, server):
        # print ("WebSocket 起動")
        pass

    def message_received(self, client, server, message):
        self.q_sentence.put(message)

    def server(self):
        PORT = 8002
        Handler = http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            url = "https://kat-subtitle.netlify.app/"
            # webbrowser.open_new(url)
            httpd.serve_forever()


if __name__ == "__main__":
    app = Websocket()
