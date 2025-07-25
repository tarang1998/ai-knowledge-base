import openai 
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


client = openai.OpenAI()

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static"



@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        language = request.form["language"]
        file = request.files["file"]

        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            audio_file = open("static/" + filename, "rb")

            transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
            )


            response = openai.chat.completions.create(
                    model="gpt-4",
                    messages = [{ "role": "system", "content": f"You will be provided with a sentence in English, and your task is to translate it into {language}" }, 
                                { "role": "user", "content": transcription.text }],
                    temperature=0,
                    max_tokens=256
                  )
            
            return response.choices[0].message.content
        
    
    return render_template("index.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)