# KAT Subtitle

![image1](images/1.gif)

KAT SubtitleはWeb Speech APIを用いて認識した音声を、VR Chatに文字情報として送信するためのソフトウェアです。また自動翻訳や外部ソフトを利用することでの音声合成も可能です。

## 動作環境

Kuretan Avatar Text

Google Chrome(Web Speech APIに利用します)

## 導入方法

リリースまたはBoothからKAT Subtitlesをダウンロード

KAT_Subtitle.exeを起動

### Charmapmakerを利用する場合

KAT_Subtitle.exeと同じ階層のフォルダにCharmap Makerで作成したConvertlist.csvを導入してください。

## 主な機能

- 音声を入力
- 入力内容の相互翻訳
- 外部ソフトを用いた音声合成

## 使い方

### 音声入力

KAT_Subtitle.exeを起動すると、Chromeのウインドウとエディタが起動します。

![image1](images/1.gif)

![image3](images/3.gif)

ChromeのウインドウはWeb Speech APIを用いた音声認識およびGoogle translateによる翻訳に使用します。マイクのアイコンを押すと音声認識が開始されます。認識された音声は
画面の中央部に表示された後、二つ目のウインドウに送られてから、VR Chatに送られます。使用上32文字以上の文章は表示できないため、長文でしゃべることはできません。

### 手動入力

KAT Subtitleはタイピングによる入力にも採用しています。エディタ上に、直接文字を入力してください。文章の最後が「。」または「？」で終了した場合、エディタ上の文章はリセットされます。右側のClearボタンを押しても、テキストを消すことができます。Windows11をご利用の方は、windows11の標準音声入力をすることも可能です。文字入力欄を選択中にWindows+Hを押すと、音声入力が開始されます。音声入力の設定から句読点の自動挿入をオンにすると、文章が終わると自動的に入力内容がクリアされます。これにより一々文章を削除することなく、スムーズにしゃべり続けることができます。Web Speech APIとWindows11標準の音声入力の精度は大差ありませんので、お好みのほうをご利用ください。またいずれの音声入力も外部での音声認識を行っているため、部外者に内容が伝わる可能性があることをご留意ください。

### 翻訳

![imager2](images/2.gif)
KAT Subtileは日本語以外にも英語、ドイツ語、中国語、韓国語などの多くの言語に対応しています。Chromeのウインドウの画面の中央部、聞き取る言語の右側にあるプルダウンメニューから聞き取る言語を指定します。翻訳すると書かれたボタンをクリックすると翻訳に関する項目が現れます。翻訳元言語と翻訳先言語を指定してください。音声認識と翻訳では使用しているAPIが異なるため、手動で翻訳元言語は指定してください。

### 音声合成

KAT Subtitleは[棒読みちゃん](https://chi.usamimi.info/Program/Application/BouyomiChan/)に対応しています。棒読みちゃんに[棒読みちゃんWebSocketプラグイン](https://github.com/ryujimiya/Plugin_BymChnWebSocket)を導入することで棒読みちゃんに発声させることができます。翻訳をオフにしている際は認識した音声を、翻訳をオンにした際は翻訳語の文章を読み上げてくれます。

## Q&A

Q.文字化けする・文字が表示されない

A.OSCが有効になっているか・Convertlistが破損していないか・Convertlistが現在使用しているシェーダーの画像に対応しているかを確認してください。

Q.Chromeの読み込みがいつまでも終わらない

A.アプリを再起動してください。

## 開発者向け情報

テキスト表示部分に関してはPython,音声認識部分に関しては[Web Speech API](https://developer.chrome.com/blog/voice-driven-web-apps-introduction-to-the-web-speech-api/)を、翻訳に関して[Apps Script  \|  Google Developers](https://developers.google.com/apps-script)の翻訳機能を利用しています。テキストを表示させる部分の処理については[KillFrenzy Avatar Text OSC App](https://github.com/killfrenzy96/KatOscApp)の方法を流用しています。また棒読みちゃんとの連携に関しては[棒読みちゃんWebSocketプラグイン](https://github.com/ryujimiya/Plugin_BymChnWebSocket)を利用しています。


## 使用しているライブラリ

[KillFrenzy Avatar Text OSC App](https://github.com/killfrenzy96/KatOscApp)

[Web Speech API](https://developer.chrome.com/blog/voice-driven-web-apps-introduction-to-the-web-speech-api/)

[棒読みちゃんWebSocketプラグイン](https://github.com/ryujimiya/Plugin_BymChnWebSocket)

## ライセンス

本ソフトウェアはGNU General Public Licenseで配布しています。

## なぜこのソフトを作成したか

私がVR Chatを始めたきっかけは英語の勉強をするためです。VRチャット上には語学の勉強に熱心な人がたくさんいます。彼らは熱心に言語交換をしていますが、しばしばうまくコミュニケーションがとれないことがあります。そんな際にVR Chat上に任意の文字を表示できたり、翻訳をしてくれる機能があったら便利だと思い、このアプリを作成しました。KAT Subtitleの文字を表示する部分に関しては、かなりの部分をKillFrenzy Avatar Text OSC Appのソースコードを流用しています。このアプリがなければ、私はこのソフトの開発を思いつかなったでしょう。またGoogleが音声認識機能や翻訳機能を無償で公開していなければこのソフトの開発自体が不可能でした。この場を借りて、KillFrenzy氏、Googleまたテストに協力してくれたVR Chat上での多くのフレンドに感謝の意を述べさせていただきます。ありがとうございました。

## 寄付

KAT SubtitleはKuretan個人により開発されたソフトウェアです。もしKAT Subtitleを気に入っていただけたら、Boothでの購入や干し芋入りスト、Patronなどbuymeacoffee等を通じて支援がいただけたらありがたいです。勿論TwitterやVR Chat上での感想やコメント・フィードバック、あるいはGithub上でのプルリクエスト等お待ちしています。