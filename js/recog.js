  //やってること
    //Webspeech APIを叩いて、音声を認識させる
    //音声を翻訳
    //翻訳した内容を棒読みちゃんに投げる
    const recognition = new webkitSpeechRecognition()//ブラウザ内臓なのでキーいらない
    const  url_base="https://script.google.com/macros/s/AKfycbwQQzNfDj9-Oou2-xTC7lrH6WbQakX2La89fVJ6z_i7XiX5WhoWUZIrbxDIFKkI6AzG/exec?text="
    let xhr = new XMLHttpRequest();
    recognition.continuous = true;//途中で切れなくするため
    recognition.interimResults = true;
    recognition.lang = 'ja'//言語指定
    let sock = new WebSocket('ws://127.0.0.1:5001');
    let bouyomiChanClient = new BouyomiChanClient();//棒読みちゃん呼び出し
    // let sock = new WebSocket('ws://localhost:50002');
    recognition.start()//開始処理
    recognition.onend = function() {//認識がストップしたら再起動
    translation_span.innerHTML ='Speech recognition service disconnected';
    recognition.start()
    translation_span.innerHTML ='Speech recognition service start';
  }
    recognition.onresult = function(event) 
    {
    var final_transcript="";//聞き取った内容
    var interim_transcript="";//いらない？
    for (var i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        final_transcript += event.results[i][0].transcript;
      } else {
        interim_transcript += event.results[i][0].transcript;
      }
    }
    final_span.innerHTML =final_transcript;
    if (final_transcript!=""){
      var lang_from="ja"
      // var lang_to="cmn-Hans-CN"
      var lang_to="en"
      var url=url_base+final_transcript+"&source="+lang_from+"&target="+lang_to
      xhr.open('GET', url);
      xhr.send();
      xhr.onload=function(){
          if (xhr.status != 200) { // レスポンスの HTTP ステータスを解析
          alert(`Error ${xhr.status}: ${xhr.statusText}`); // e.g. 404: Not Found
        } else { // show the result
          // alert(`${xhr.response}`); // responseText is the server
      //   }
          console.log(url);
          translation_span.innerHTML =xhr.response;
          console.log('socket open');
          var send_text=xhr.response;
          // var send_text=final_transcript;
          sock.send(send_text);//KAT に文章を送る
          bouyomiChanClient.talk(send_text);//棒読みちゃんに文章を送る
      }
      }

}
}