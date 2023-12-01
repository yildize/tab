!nvidia-smi

#!pip install ctransformers
!pip install ctransformers[cuda] huggingface-hub # If GPU acceleration is needed

!pip install transformers

from google.colab import drive
drive.mount('/content/drive')

from ctransformers import AutoModelForCausalLM
# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
llm = AutoModelForCausalLM.from_pretrained("TheBloke/WizardLM-70B-V1.0-GGUF", model_file="wizardlm-70b-v1.0.Q3_K_L.gguf", model_type="llama",  gpu_layers=50)

# Save the model to a specified directory
llm.save_pretrained("/content/drive/MyDrive/LargeLLM")

llm = AutoModelForCausalLM.from_pretrained("/content/drive/MyDrive/LargeLLM", model_type="llama",  gpu_layers=50)

!pip install flask ngrok
!pip install flask_ngrok


from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)
@app.route('/ask', methods=['POST'])
def ask_model():
    # Assuming the incoming data is JSON with UTF-8 encoding
    data = request.data.decode('utf-8')
    # Convert the JSON string to a Python dictionary
    json_data = json.loads(data)
    query = json_data["query"]
    #find_non_printable_chars(query)
    cleaned_inp = re.sub(r'[^\x20-\x7E\nçÇşŞğĞıİöÖüÜ]', '', query)
    llm_answer =  llm(cleaned_inp)
    return jsonify({'answer': llm_answer})

!wget -q https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
!unzip -q ngrok-stable-linux-amd64.zip
!./ngrok authtoken 2YnMdqu3LOPhsWZEF8xygexQD2C_7b6dateCU5YaVnF7eH4ak

from flask_ngrok import run_with_ngrok

run_with_ngrok(app)  # Start ngrok when the app is run
app.run()