from flask import Flask, request, render_template_string
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

html_template = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>음성 번역기</title>
  <script>
    function startListening() {
      const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
      recognition.lang = "ko-KR";
      recognition.start();

      recognition.onresult = function(event) {
        const text = event.results[0][0].transcript;
        document.getElementById("user_input").value = text;
      };
    }

    function speak(text, lang) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = lang;
      window.speechSynthesis.speak(utterance);
    }
  </script>
</head>
<body>
  <h2>🎙 음성으로 말하거나 직접 입력하세요:</h2>
  <form method="POST">
    <input type="text" name="user_input" id="user_input" placeholder="번역할 문장" size="50">
    <button type="button" onclick="startListening()">🎤 음성 입력</button><br><br>
    <label>번역할 언어 선택:</label>
    <select name="target_lang" id="target_lang">
      <option value="en">영어</option>
      <option value="ja">일본어</option>
      <option value="zh-CN">중국어(간체)</option>
    </select>
    <input type="submit" value="번역">
  </form>

  {% if result %}
    <h3>번역 결과:</h3>
    <p id="output">{{ result }}</p>
    <button onclick="speak('{{ result }}', '{{ target_lang }}')">🔊 읽어주기</button>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    target_lang = "en"
    if request.method == "POST":
        text = request.form["user_input"]
        target_lang = request.form["target_lang"]
        translated = translator.translate(text, src='ko', dest=target_lang)
        result = translated.text
    return render_template_string(html_template, result=result, target_lang=target_lang)

if __name__ == "__main__":
    app.run()


