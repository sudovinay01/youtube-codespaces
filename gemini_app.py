from google import genai
from google.genai import types
from dotenv import load_dotenv
from flask import Flask, render_template_string, request
import os

app = Flask(__name__)


def validate_api_key(api_key):
    if not api_key:
        return False, "Please set the GEMINI_API_KEY environment variable"

    try:
        test_client = genai.Client(api_key=api_key)
        # Make a simple test call
        test_client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents='test'
        )
        return True, None
    except Exception:
        return False, "Invalid API key"


load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
is_valid_key, error_message = validate_api_key(api_key)
client = genai.Client(api_key=api_key) if is_valid_key else None

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
        {% if not is_valid_key %}
        <div class="response">{{ response }}</div>
        {% else %}
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
        {% endif %}
    </div>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def home():
    prompt = ''
    response_text = ''

    if not is_valid_key:
        response_text = error_message
    elif request.method == 'POST':
        prompt = request.form.get('prompt', '')
        if prompt:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=prompt
            )
            response_text = response.text

    return render_template_string(html_template,
                                  prompt=prompt,
                                  response=response_text,
                                  is_valid_key=is_valid_key)


if __name__ == '__main__':
    app.run(debug=True)
