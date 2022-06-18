import pyvcroid2
import winsound
import sys

#ハンドジェスチャーに応じて声質や音声を変える。
#OSCで調整できる 速さやピッチの調整も可能

class Make_sound():
    def __init__(self,_is_standard=True,_who_speak=3):
            self.vc=pyvcroid2.VcRoid2() 
            # Load language library
            self.lang_list = self.vc.listLanguages()
            # print(lang_list)
            # if "standard" in self.lang_list:
            if _is_standard:
                # self.vc.loadLanguage("standard")
                self.vc.loadLanguage("standard_kansai")
            elif 0 < len(self.lang_list):
                self.vc.loadLanguage(self.lang_list[0])
            else:
                raise Exception("No language library")
            # # Set parameters
            # Load Voice
            self.voice_list =self.vc.listVoices()
            if 0 < len(self.voice_list):
                # print(self.voice_list)
                self.vc.loadVoice(self.voice_list[_who_speak])
            else:
                raise Exception("No voice library")
            self.vc.param.volume = 1.23
            self.vc.param.speed = 0.987
            self.vc.param.pitch = 1.111
            self.vc.param.emphasis = 0.893
            self.vc.param.pauseMiddle = 80
            self.vc.param.pauseLong = 100
            self.vc.param.pauseSentence = 200
            self.vc.param.masterVolume = 1.123
            print("Voiceroid2読み込み成功")
            
    def speech(self,text):
        # Text to speech
        # text="".join(sys.argv[1:])
        speech, tts_events = self.vc.textToSpeech(text)
        winsound.PlaySound(speech, winsound.SND_MEMORY)
        # with open('tes.wav', mode='wb') as tes:
        #     tes.write(speech)

if __name__ == "__main__":
    # app=Make_sound(_who_speak=6)
    # # app.vc.param.speed = 1.987
    # # app.vc.param.pitch = 1.911
    # # text="".join(sys.argv[1:])
    # text="オブジェクトの削除について"
    # app.speech(text)
    # del app
    # app=Make_sound(_who_speak=7)
    # # text="".join(sys.argv[1:])
    # text="123"
    # app.speech(text)

    with open(r"D:\Documents\投稿動画\素材\kiritan_exVOICE\0よく使うやつ\なにいってんだこいつ。.wav", 'rb') as f:
        data = f.read()
        winsound.PlaySound(data, winsound.SND_MEMORY)