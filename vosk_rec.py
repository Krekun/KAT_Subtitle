from posixpath import split
import queue
import sounddevice as sd
import vosk
import sys
import threading
import KatOscApp
import asyncio

class Vosk_rec():
    def __init__(self) -> None:
        self.q = queue.Queue()
        self.q_sentence=queue.Queue()
        self.model=vosk.Model("model")
        #これなら動く　なぜかモデルの読み込みに失敗していたのでこうなった。
        #websocketで渡してもいいし
        thread1=threading.Thread(target=KatOscApp.KatOscApp,kwargs={"loop":asyncio.get_event_loop()})
        thread1.start()
        thread2=threading.Thread(target=self.recognize)
        thread2.start()

        # self.recognize()

    def recognize(self):
        try:

            samplerate=None
            with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=None, dtype='int16',
                                        channels=1, callback=self.callback):
                print('#' * 80)
                print('Press Ctrl+C to stop the recording')
                print('#' * 80)
                rec = vosk.KaldiRecognizer(self.model, 44100)

                while True:
                    data = self.q.get()
                    if rec.AcceptWaveform(data):
                        temp=rec.Result().split(":")[1].strip('\"').strip("}").strip("/n").split(" ")
                        temp="".join(temp)
                        print(temp)
                        self.q_sentence.put(temp)
                        # return "".join(temp)
                    else:
                        pass

        except KeyboardInterrupt:
            print('\nDone')
            self.parser.exit(0)

    def callback(self,indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

if __name__=="__main__":
    app=Vosk_rec()
    # app.recognize()
    # pass