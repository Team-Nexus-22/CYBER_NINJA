from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
warnings.filterwarnings('ignore')
from feature import FeatureExtraction
import google.generativeai as genai
import nltk

app = Flask(__name__)
file = open("pickle/model.pkl","rb")
gbc = pickle.load(file)
file.close()

name="CYBER NINJA"
#dashboard route
@app.route('/')
def home():
    return render_template('index.html',title=name)

#phishing
@app.route("/phishing-url-detector", methods=["GET", "POST"])
def phishing_url_detector():
    if request.method == "POST":

        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30) 

        y_pred =gbc.predict(x)[0]
        #1 is safe       
        #-1 is unsafe
        y_pro_phishing = gbc.predict_proba(x)[0,0]
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]
        # if(y_pred ==1 ):
        pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        return render_template('phishingURLDetector.html',xx =round(y_pro_non_phishing,2),url=url )
    return render_template("phishingURLDetector.html", xx =-1)

api_key = "AIzaSyBVbV0KNNMV70FVebcWm2Vn5AoNlXAvNlA"  
genai.configure(api_key=api_key)


model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

nltk.download('punkt')

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

def format_response(response_text):
    replacements = {"gemini": "G-AI", "google": "Nexus"}
    formatted_response = response_text
    for key, value in replacements.items():
        formatted_response = formatted_response.replace(key, value)
    
    lines = formatted_response.split('\n')

    formatted_response = ''
    for line in lines:
        if '**' in line:
            segments = line.split('**')
            for i, segment in enumerate(segments):
                if i % 2 == 1:
                    segments[i] = f'<b>{segment}</b>'
            line = ''.join(segments)
        formatted_response += f'{line}<br>'

    return formatted_response

def custom_response(question):
    if "your name" in question.lower() or "what is your name" in question.lower():
        return "My name is G-AI."
    else:
        return None



@app.route('/g-ai')
def g_ai():
    return render_template('g_ai.html', title=name)

@app.route('/ask', methods=['POST'])
def ask_question():
    user_input = request.form['question']

    if user_input.lower() == 'quit':
        return "Exiting the chatbot. Goodbye!"

    custom_resp = custom_response(user_input)
    if custom_resp:
        return custom_resp

    response = get_gemini_response(user_input)
    response_text = ''
    for chunk in response:
        response_text += chunk.text + ' '

    formatted_response = format_response(response_text)

    return formatted_response

if __name__ == '__main__':
    app.run(debug=True)