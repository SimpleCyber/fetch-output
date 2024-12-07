from flask import Flask, request, jsonify
import openai
import os
import json

app = Flask(__name__)

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-4"

# System prompt definition
system_prompt = """
    You are an AI model that detects the given  is profile fake or not based on the number of followers , following , bio , verified or not, username trying to impersonate some famous user names , from the post's caption events in real-time or in the past if the data , number of posts etc. You will be provided with the input of users social media profile information and posts and your goal is to respond with a structured solution in this format:
    <div class="final_output">
        <h3> Fake post detection:<h3>
        <table>
            <tr>
                <td>Fake or propaganda information</td>
                <td><span class="propaganda">(percentage out of 100)</span></td>
            </tr>
            <tr>
                <td>Extremist</td>
                <td><span class="Extremist">(percentage out of 100)</span></td>
            </tr>
            <tr>
                <td>Spam message</td>
                <td><span class="Spam">(percentage out of 100)</span></td>
            </tr>
            <tr>
                <td>Violent or hate speech or toxic</td>
                <td><span class="hate">(percentage out of 100)</span></td>
            </tr>
            <tr>
                <td>Impersonate account</td>
                <td><span class="Impersonate">(percentage out of 100)</span></td>
            </tr>
            <tr>
                <td>Incomplete profile</td>
                <td><span class="Incomplete">(percentage out of 100)</span></td>
            </tr>
        </table>
        <li>Percentage of risk :<span class="risk"> (percentage out of 100)</span></li>
        <strong>Reason:</strong>
            If the profile belongs to any of these 6 categories then why just in 10-20 words.
        <strong>Conclusion: </strong>
            Just one precise summary point.
            
            </div>
"""

@app.route('/command', methods=['POST'])
def process_command():
    try:
        # Retrieve the command from the request
        data = request.get_json()
        command = data.get('command', 'default')
        
        # OpenAI API call to generate HTML
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate HTML for the command: {command}"}
            ]
        )

        # Extract and return the HTML content
        generated_html = response["choices"][0]["message"]["content"]
        return jsonify({"html": generated_html})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
