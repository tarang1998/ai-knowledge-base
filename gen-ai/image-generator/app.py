import openai 
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
client = openai.OpenAI()


app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html', )
  

@app.route('/generateimages/<prompt>')
def generate(prompt):
  print("prompt:", prompt)
  response = client.images.generate(prompt=prompt, n=5, size="256x256") 

  # Extract image URLs from response
  image_urls = [image.url for image in response.data]
    
  # Print URLs for debugging
  print("Generated Images:", image_urls)
    
  # Return only URLs in JSON format
  return jsonify({"data": image_urls})


app.run(host='0.0.0.0', debug= True, port=8080)