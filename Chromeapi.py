from websocket_server import WebsocketServer
import threading
import KatOscApp
import asyncio
import queue
import localserver
import webbrowser


class Websocket():
    def __init__(self) -> None:
        self.q = queue.Queue()
        self.q_sentence=queue.Queue()
        thread1=threading.Thread(target=KatOscApp.KatOscApp,kwargs={"loop":asyncio.get_event_loop(),"queue":self.q_sentence,"_use_chrome":True})
        thread1.start()
        thread2=threading.Thread(target=localserver.localserver)
        thread2.start()

        server = WebsocketServer(port=5001, host='127.0.0.1')
        server.set_fn_new_client(self.new_client)
        server.set_fn_message_received(self.message_received)
        url="http://localhost:8001/"
        webbrowser.open(url)
        server.run_forever()
    def new_client(self,client, server):
        print ("接続しました")

    def message_received(self,client, server, message):
        # print (message)
        self.q_sentence.put(message)

if __name__=="__main__":
    app=Websocket()