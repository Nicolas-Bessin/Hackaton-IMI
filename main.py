from flask import Flask, render_template, request, redirect
import os
from src.utils.ask_question_to_pdf import ask_question_to_pdf, gpt3_completion, split_text, read_pdf


app = Flask(__name__)

context = " "

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/prompt", methods=["POST"])
def prompt():
    global context 
    question = request.form["prompt"]
     answer = gpt3_completion(context + "\n" + question)
    context = context + "\n" + question + "\n" + answer
    return {"answer" : answer }, 200

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    try:
        os.mkdir("database")
    except:
        pass
    filepath = f"database/{file.filename}"
    file.save(filepath)

    document = read_pdf(filepath)
    chunks = split_text(document)

    return redirect("/")
