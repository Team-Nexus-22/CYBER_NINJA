from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

name="CYBER NINJA"
#dashboard route
@app.route('/')
def home():
    return render_template('index.html',title=name)
@app.route('/phishingdetection')
def phishing():
    return render_template('phishingdetection.html')


if __name__ == '__main__':
    app.run(debug=True)