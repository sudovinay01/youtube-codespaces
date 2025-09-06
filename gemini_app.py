from google import genai
from google.genai import types
from dotenv import load_dotenv
from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

# HTML template for the web page
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Gemini AI Chat</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { margin-top: 20px; }
        textarea { width: 100%; height: 100px; margin-bottom: 10px; }
        .response { margin-top: 20px; padding: 10px; background-color: #f0f0f0; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Gemini AI Chat</h1>
    <div class="container">
        <form method="POST">
            <textarea name="prompt" placeholder="Enter your prompt here...">{{ prompt }}</textarea><br>
            <input type="submit" value="Send">
        </form>
        {% if response %}
        <div class="response">
            <strong>Response:</strong><br>
            {{ response }}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def home():
    prompt = ''
    response_text = ''

    if request.method == 'POST':
        prompt = request.form.get('prompt', '')
        if prompt:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=prompt
            )
            response_text = response.text

    return render_template_string(html_template, prompt=prompt, response=response_text)


if __name__ == '__main__':
    app.run(debug=True)
