var langs_recognition =
  [['Afrikaans', ['af-ZA']],
  ['Bahasa Indonesia', ['id-ID']],
  ['Bahasa Melayu', ['ms-MY']],
  ['Català', ['ca-ES']],
  ['Čeština', ['cs-CZ']],
  ['Deutsch', ['de-DE']],
  ['English', ['en-US', 'United States'],
    ['en-AU', 'Australia'],
    ['en-CA', 'Canada'],
    ['en-IN', 'India'],
    ['en-NZ', 'New Zealand'],
    ['en-ZA', 'South Africa'],
    ['en-GB', 'United Kingdom']],
  ['Español', ['es-AR', 'Argentina'],
    ['es-BO', 'Bolivia'],
    ['es-CL', 'Chile'],
    ['es-CO', 'Colombia'],
    ['es-CR', 'Costa Rica'],
    ['es-EC', 'Ecuador'],
    ['es-SV', 'El Salvador'],
    ['es-ES', 'España'],
    ['es-US', 'Estados Unidos'],
    ['es-GT', 'Guatemala'],
    ['es-HN', 'Honduras'],
    ['es-MX', 'México'],
    ['es-NI', 'Nicaragua'],
    ['es-PA', 'Panamá'],
    ['es-PY', 'Paraguay'],
    ['es-PE', 'Perú'],
    ['es-PR', 'Puerto Rico'],
    ['es-DO', 'República Dominicana'],
    ['es-UY', 'Uruguay'],
    ['es-VE', 'Venezuela']],
  ['Euskara', ['eu-ES']],
  ['Français', ['fr-FR']],
  ['Galego', ['gl-ES']],
  ['Hrvatski', ['hr_HR']],
  ['IsiZulu', ['zu-ZA']],
  ['Íslenska', ['is-IS']],
  ['Italiano', ['it-IT', 'Italia'],
    ['it-CH', 'Svizzera']],
  ['Magyar', ['hu-HU']],
  ['Nederlands', ['nl-NL']],
  ['Norsk bokmål', ['nb-NO']],
  ['Polski', ['pl-PL']],
  ['Português', ['pt-BR', 'Brasil'],
    ['pt-PT', 'Portugal']],
  ['Română', ['ro-RO']],
  ['Slovenčina', ['sk-SK']],
  ['Suomi', ['fi-FI']],
  ['Svenska', ['sv-SE']],
  ['Türkçe', ['tr-TR']],
  ['български', ['bg-BG']],
  ['Pусский', ['ru-RU']],
  ['Српски', ['sr-RS']],
  ['한국어', ['ko-KR']],
  ['中文', ['cmn-Hans-CN', '普通话 (中国大陆)'],
    ['cmn-Hans-HK', '普通话 (香港)'],
    ['cmn-Hant-TW', '中文 (台灣)'],
    ['yue-Hant-HK', '粵語 (香港)']],
  ['日本語', ['ja-JP']],
  ['Lingua latīna', ['la']]];

var langs_translate =
  [['Japanese', ['ja']],
  ['English', ['en']],
  ['Afrikaans', ['af']],
  ['Albanian', ['sq']],
  ['Amharic', ['am']],
  ['Arabic', ['ar']],
  ['Armenian', ['hy']],
  ['Azerbaijani', ['az']],
  ['Basque', ['eu']],
  ['Belarusian', ['be']],
  ['Bengali', ['bn']],
  ['Bosnian', ['bs']],
  ['Bulgarian', ['bg']],
  ['Catalan', ['ca']],
  ['Cebuano', ['ceb']],
  ['Chinese (Simplified)', ['zh-CN']],
  ['Chinese (Traditional)', ['zh-TW']],
  ['Corsican', ['co']],
  ['Croatian', ['hr']],
  ['Czech', ['cs']],
  ['Danish', ['da']],
  ['Dutch', ['nl']],
  ['Esperanto', ['eo']],
  ['Estonian', ['et']],
  ['Finnish', ['fi']],
  ['French', ['fr']],
  ['Frisian', ['fy']],
  ['Galician', ['gl']],
  ['Georgian', ['ka']],
  ['German', ['de']],
  ['Greek', ['el']],
  ['Gujarati', ['gu']],
  ['Haitian Creole', ['ht']],
  ['Hausa', ['ha']],
  ['Hawaiian', ['haw']],
  ['Hebrew', ['he']],
  ['Hindi', ['hi']],
  ['Hmong', ['hmn']],
  ['Hungarian', ['hu']],
  ['Icelandic', ['is']],
  ['Igbo', ['ig']],
  ['Indonesian', ['id']],
  ['Irish', ['ga']],
  ['Italian', ['it']],
  ['Javanese', ['jv']],
  ['Kannada', ['kn']],
  ['Kazakh', ['kk']],
  ['Khmer', ['km']],
  ['Kinyarwanda', ['rw']],
  ['Korean', ['ko']],
  ['Kurdish', ['ku']],
  ['Kyrgyz', ['ky']],
  ['Lao', ['lo']],
  ['Latin', ['la']],
  ['Latvian', ['lv']],
  ['Lithuanian', ['lt']],
  ['Luxembourgish', ['lb']],
  ['Macedonian', ['mk']],
  ['Malagasy', ['mg']],
  ['Malay', ['ms']],
  ['Malayalam', ['ml']],
  ['Maltese', ['mt']],
  ['Maori', ['mi']],
  ['Marathi', ['mr']],
  ['Mongolian', ['mn']],
  ['Myanmar (Burmese)', ['my']],
  ['Nepali', ['ne']],
  ['Norwegian', ['no']],
  ['Nyanja (Chichewa)', ['ny']],
  ['Odia (Oriya)', ['or']],
  ['Pashto', ['ps']],
  ['Persian', ['fa']],
  ['Polish', ['pl']],
  ['Portuguese (Portugal, Brazil)', ['pt']],
  ['Punjabi', ['pa']],
  ['Romanian', ['ro']],
  ['Russian', ['ru']],
  ['Samoan', ['sm']],
  ['Scots Gaelic', ['gd']],
  ['Serbian', ['sr']],
  ['Sesotho', ['st']],
  ['Shona', ['sn']],
  ['Sindhi', ['sd']],
  ['Sinhala (Sinhalese)', ['si']],
  ['Slovak', ['sk']],
  ['Slovenian', ['sl']],
  ['Somali', ['so']],
  ['Spanish', ['es']],
  ['Sundanese', ['su']],
  ['Swahili', ['sw']],
  ['Swedish', ['sv']],
  ['Tagalog (Filipino)', ['tl']],
  ['Tajik', ['tg']],
  ['Tamil', ['ta']],
  ['Tatar', ['tt']],
  ['Telugu', ['te']],
  ['Thai', ['th']],
  ['Turkish', ['tr']],
  ['Turkmen', ['tk']],
  ['Ukrainian', ['uk']],
  ['Urdu', ['ur']],
  ['Uyghur', ['ug']],
  ['Uzbek', ['uz']],
  ['Vietnamese', ['vi']],
  ['Welsh', ['cy']],
  ['Xhosa', ['xh']],
  ['Yiddish', ['yi']],
  ['Yoruba', ['yo']],
  ['Zulu', ['zu']]
  ];

for (var i = 0; i < langs_recognition.length; i++) {
  select_language.options[i] = new Option(langs_recognition[i][0], i);
}
$("#select_language").val(30);
UpdateCountry();
ShowInfo('info_start');

for (var i = 0; i < langs_translate.length; i++) {
  select_lang_from.options[i] = new Option(langs_translate[i][0], langs_translate[i][1]);
  select_lang_to.options[i] = new Option(langs_translate[i][0], langs_translate[i][1]);
}

let xhr = new XMLHttpRequest();
try {
  var GAS_url_base = window.localStorage.getItem('GAS_URL').replace(/\"/g, "");
} catch (e) {
  var GAS_url_base = ""
}
// if (GAS_url_base!=""){
//   test_translate();
// }
$('#GAS_URL').val(GAS_url_base);
$('#GAS_URL').change(function () {
  var new_url = $(this).val();
  GAS_url_base = new_url;
  console.log(new_url);
  let jsonData = JSON.stringify(new_url);
  localStorage.setItem('GAS_URL', jsonData);
  test_translate();
});

let sock = new WebSocket('ws://127.0.0.1:5001');
sock.onerror = function (error) {
  alert("WebSocketに接続できません。リロードしてください。\nリロード後もこのエラーが出る場合はKAT Subtitleを再起動してください。");
};
let bouyomiChanClient = new BouyomiChanClient();//棒読みちゃん呼び出し
var is_translate = false;
var is_subtitle = true;
var is_Makevoice = true;
var final_transcript = '';
var recognizing = false;
var ignore_onend;
var start_timestamp;
if (!('webkitSpeechRecognition' in window)) {
  upgrade();
} else {
  start_button.style.display = 'inline-block';
  var recognition = new webkitSpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;

  recognition.onstart = function () {
    ShowInfo('info_speak_now');
    start_img.src = 'images/mic-animate.gif';
  };

  recognition.onerror = function (event) {
    if (event.error == 'no-speech') {
      start_img.src = 'images/mic.gif';
      ShowInfo('info_no_speech');
      ignore_onend = true;
    }
    if (event.error == 'audio-capture') {
      start_img.src = 'images/mic.gif';
      ShowInfo('info_no_microphone');
      ignore_onend = true;
    }
    if (event.error == 'not-allowed') {
      if (event.timeStamp - start_timestamp < 100) {
        ShowInfo('info_blocked');
      } else {
        ShowInfo('info_denied');
      }
      ignore_onend = true;
    }
  };

  recognition.onend = function () {
    if (recognizing) {
      recognition.start()
    }
    else {
      start_img.src = 'images/mic.gif';
      ShowInfo('');
    }

  }

  recognition.onresult = function (event) {
    var interim_transcript = '';
    var final_transcript = '';
    for (var i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        final_transcript += event.results[i][0].transcript;
      } else {
        interim_transcript += event.results[i][0].transcript;
      }
    }
    final_transcript = capitalize(final_transcript);
    final_span.innerHTML = linebreak(final_transcript);
    interim_span.innerHTML = linebreak(interim_transcript);
    if (final_transcript != "") {
      if (is_translate) {
        Google_translate(final_transcript);
      }
      else {
        Send_texts(final_transcript);
      }

    }
  };
}

function UpdateCountry() {
  for (var i = select_dialect.options.length - 1; i >= 0; i--) {
    select_dialect.remove(i);
  }
  var list = langs_recognition[select_language.selectedIndex];
  for (var i = 1; i < list.length; i++) {
    select_dialect.options.add(new Option(list[i][1], list[i][0]));
  }
  select_dialect.style.visibility = list[1].length == 1 ? 'hidden' : 'visible';
}


function Google_translate(final_transcript) {
  var lang_from = select_lang_from.value;
  var lang_to = select_lang_to.value;
  var url = GAS_url_base + "?text=" + final_transcript + "&source=" + lang_from + "&target=" + lang_to;
  xhr.open('GET', url);
  xhr.send();
  console.log("Xhrsent")
  xhr.onerror = function () {
    alert("翻訳に問題が発生しました。")
  }
  xhr.onload = function () {
    if (xhr.status != 200) { // レスポンスの HTTP ステータスを解析
      alert(`Error ${xhr.status}: ${xhr.statusText}`); // e.g. 404: Not Found
    }
    else {
      console.log(url);
      translation_span.innerHTML = xhr.response;
      var send_text = xhr.response;
      console.log(send_text);
      Send_texts(send_text);
    }
  }
}



function Send_texts(final_transcript) {
  var send_text = final_transcript;
  if (is_subtitle) {
    sock.send(send_text);//KAT に文章を送る
  }
  if (is_Makevoice) {
    bouyomiChanClient.talk(send_text);//棒読みちゃんに文章を送る
  }
}

function test_translate() {
  if (GAS_url_base == "") {
    alert("翻訳機能の利用には設定が必要です。\nReadmeを確認してください。")
  }
  else {
    var url = GAS_url_base + "?text=" + "テスト" + "&source=ja&target=en";
    xhr.open('GET', url);
    xhr.send();
    xhr.onerror = function () {
      alert("翻訳のテストに失敗しました。URLが正しいか確認してください。");
    }
    xhr.onload = function () {
      if (xhr.status != 200) { // レスポンスの HTTP ステータスを解析
        alert(`Error ${xhr.status}: ${xhr.statusText}`); // e.g. 404: Not Found
      }
      else {
        console.log(url);
        if (xhr.response != "test") {
          alert("翻訳に問題が発生しました。URLが正しいか確認してください。")
        }
        else {
          console.log("Translation test worked successfully")
        }

      }
    }
  }
}


function upgrade() {
  start_button.style.visibility = 'hidden';
  ShowInfo('info_upgrade');
}

var two_line = /\n\n/g;
var one_line = /\n/g;
function linebreak(s) {
  return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
}

var first_char = /\S/;
function capitalize(s) {
  return s.replace(first_char, function (m) { return m.toUpperCase(); });
}


function startButton(event) {
  if (recognizing) {
    recognizing = false;
    recognition.stop();
    return;
  }
  final_transcript = '';
  recognition.lang = select_dialect.value;
  recognition.start();
  recognizing = true;
  ignore_onend = false;
  final_span.innerHTML = '';
  interim_span.innerHTML = '';
  start_img.src = 'images/mic-slash.gif';
  ShowInfo('info_allow');
  ShowButtons('none');
  start_timestamp = event.timeStamp;
}

function ShowInfo(s) {
  if (s) {
    for (var child = info.firstChild; child; child = child.nextSibling) {
      if (child.style) {
        child.style.display = child.id == s ? 'inline' : 'none';
      }
    }
    info.style.visibility = 'visible';
  } else {
    info.style.visibility = 'hidden';
  }
}

var current_style;
function ShowButtons(style) {
  if (style == current_style) {
    return;
  }
  current_style = style;
}

$('#select_language').change(function () {
  recognition.lang = select_dialect.value;
  recognition.stop();
});
$('#select_dialect').change(function () {
  recognition.lang = select_dialect.value;
  recognition.stop();
});

$("#div_translate").hide();
function translate_button_click() {
  const div_translate = document.getElementById("div_translate");

  if (div_translate.style.display == "none") {
    is_translate = true;
    $('#translate_button').val("Translate OFF");
    // test_translate();
  } else {
    is_translate = false;
    $('#translate_button').val("Translate ON");
  }
  $("#div_translate").toggle("fast");

}

$('#div_setting').hide();
function setting_button_click() {
  $("#div_setting").toggle("fast");
}

$('#Subtitle_whether').change(function () {
  var bool = $(this).prop('checked');
  if (bool) {
    is_subtitle = true;
    console.log("Subtitle enabled")
  }
  else {
    is_subtitle = false;
    console.log("Subtitle unabled")
  }
});

$('#Makevoice_whether').change(function () {
  var bool = $(this).prop('checked');
  if (bool) {
    is_Makevoice = true;
    console.log("MakeVoice enabled");
  }
  else {
    is_Makevoice = false;
    console.log("MakedVoice unabled");
  }

});