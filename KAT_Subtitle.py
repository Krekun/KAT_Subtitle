from websocket_server import WebsocketServer
import threading
import KAT_Subtitle_Gui
import asyncio
import queue
import KAT_Subtitle_server
import webbrowser

class Websocket():
    def __init__(self) -> None:
        self.q = queue.Queue()
        self.q_sentence=queue.Queue()
        # thread1=threading.Thread(target=KAT_Subtitle_Gui.KAT_Subtitle_Gui,kwargs={"loop":asyncio.get_event_loop(),"queue":self.q_sentence,"_use_chrome":True})
        # thread1.start()
        server = WebsocketServer(port=5001, host='127.0.0.1')
        server.set_fn_new_client(self.new_client)
        server.set_fn_message_received(self.message_received)
        server.run_forever()
    def websocket(self):
        server = WebsocketServer(port=5001, host='127.0.0.1')
        server.set_fn_new_client(self.new_client)
        server.set_fn_message_received(self.message_received)


    def new_client(self,client, server):
        print ("接続しました")


    def message_received(self,client, server, message):
        print (message)
        self.q_sentence.put(message)

if __name__=="__main__":
    app=Websocket()