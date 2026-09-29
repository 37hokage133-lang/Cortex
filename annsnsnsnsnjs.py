import os
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Ключ берём из переменных окружения, а не из кода!
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enough AI</title>
    <style>
        body { background: #0a0a14; color: white; font-family: Arial; padding: 20px; }
        h1 { color: #4ecca3; text-align: center; }
        #chat { background: #1a1a2e; padding: 15px; border-radius: 12px; height: 60vh; overflow-y: scroll; margin-bottom: 15px; }
        .msg { margin-bottom: 10px; }
        .user { color: #4ecca3; }
        .ai { color: #ffffff; }
        input[type="text"] { width: 70%; padding: 12px; border-radius: 8px; border: none; background: #1a1a2e; color: white; }
        button { padding: 12px 20px; background: #4ecca3; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Enough AI</h1>
    <div id="chat">
        <div class="msg ai">Привет! Я твой ИИ. Спроси что-нибудь.</div>
    </div>
    <form method="POST" action="/">
        <input type="text" name="message" placeholder="Напиши сообщение..." required>
        <button type="submit">Отправить</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_message = request.form.get("message", "")
        if user_message:
            data = {
                "model": MODEL,
                "messages": [{"role": "user", "content": user_message}],
                "stream": False
            }
            try:
                response = requests.post(URL, headers=headers, json=data, timeout=60)
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    ai_answer = result["choices"][0]["message"]["content"]
                else:
                    ai_answer = "Ошибка API."
            except Exception as e:
                ai_answer = f"Ошибка: {e}"
            return render_template_string(HTML.replace("Привет! Я твой ИИ. Спроси что-нибудь.", 
                f"Привет! Я твой ИИ. Спроси что-нибудь.<br><b>Ты:</b> {user_message}<br><b>ИИ:</b> {ai_answer}"))
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)