from flask import Flask, render_template, request, redirect
import os
from src.utils.ask_question_to_pdf import gpt3_completion, split_text, read_pdf


app = Flask(__name__)

context = ""

def get_pdf_name():
    if not os.path.isdir("database") or not os.listdir("database"):
        return "Aucun fichier mis en ligne"
    else:
        return os.listdir("database")[0] 

@app.route("/")
def hello_world():
    return render_template("index.html", filename=get_pdf_name())


@app.route("/prompt", methods=["POST"])
def prompt():
    global context
    question = request.form["prompt"]
    doc_txt = None
    if not os.path.isdir("database") or not os.listdir("database"):
        return {"answer" : "Pas de fichier mis en ligne"}, 200
    else:
        filename = "database/" + os.listdir("database")[0]
        document = read_pdf(filename)
        doc_txt = split_text(document)[0]
    answer = gpt3_completion(context + "\n" + question, text = doc_txt)
    context = context + "\n" + question + "\n" + answer
    return {"answer": answer}, 200


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    try:
        os.mkdir("database")
    except:
        for filename in os.listdir("database"):
            os.remove(f"database/{filename}")
        pass
    filepath = f"database/{file.filename}"
    file.save(filepath)
    return redirect("/")

@app.route("/question", methods=["GET"])
def question():
    global context
    doc_txt = None
    if not os.path.isdir("database") or not os.listdir("database"):
        return {"answer" : "Pas de fichier mis en ligne"}, 200
    else:
        filename = "database/" + os.listdir("database")[0]
        document = read_pdf(filename)
        doc_txt = split_text(document)[0]
    context = context + "\n" + "Peux tu me poser une question sur ce texte ?"
    answer = gpt3_completion(context, text = doc_txt)
    context = context + "\n" + answer
    return {"answer" : answer }, 200

@app.route("/answer", methods=["POST"])
def answer():
    global context
    doc_txt = None
    if not os.path.isdir("database") or not os.listdir("database"):
        return {"answer" : "Pas de fichier mis en ligne"}, 200
    else:
        filename = "database/" + os.listdir("database")[0]
        document = read_pdf(filename)
        doc_txt = split_text(document)[0]
    answer = request.form["prompt"]
    context = context + "\n" + answer
    gpt_validation = gpt3_completion(context, text = doc_txt)
    context = context + "\n" + gpt_validation
    return {"answer" : gpt_validation }, 200
  
@app.route("/resetcontext")
def reset():
    try:
        for filename in os.listdir("database"):
            os.remove(f"database/{filename}")
    except:
        pass
    global context
    context = ""
    message = "Je suis ton AIssistant de cours personnel ! Pose-moi une question sur le cours et je te répondrai."
    return message
