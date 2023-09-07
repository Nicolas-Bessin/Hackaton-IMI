from flask import Flask, render_template, request, redirect
import os
from src.utils.ask_question_to_pdf import gpt3_completion, split_text, read_pdf

app = Flask(__name__)

context = {}

def context_to_text(json_c, get_all = True):
    textual_c = ""
    for x in json_c:
        if get_all or json_c[x][1]:
            textual_c = textual_c + json_c[x][0] + "\n"

    return textual_c


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/prompt", methods=["POST"])
def prompt():
    global context
    question = request.form["prompt"]
    doc_txt = None
    if not os.path.isdir("database") or not os.listdir("database"):
        pass
    else:
        document = read_pdf("database/current_file.pdf")
        doc_txt = split_text(document)[0]
    answer = gpt3_completion(context_to_text(context, True) + question, text = doc_txt)
    context["human" + str(len(context))] = [question, True]
    context["ai" + str(len(context))] = [answer, True]
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
    filepath = "database/current_file.pdf"
    file.save(filepath)

    document = read_pdf(filepath)
    chunks = split_text(document)

    return redirect("/")

@app.route("/question", methods=["GET"])
def question():
    global context
    doc_txt = None
    if not os.path.isdir("database") or not os.listdir("database"):
        return {"answer" : "Pas de fichier mis en ligne"}, 200
    else:
        document = read_pdf("database/current_file.pdf")
        doc_txt = split_text(document)[0]
    context["human"+ str(len(context))] = ["Peux tu me poser une question sur ce texte ?", False]
    answer = gpt3_completion(context_to_text(context, True), text = doc_txt)
    context["ai" + str(len(context))] = [answer, True]
    return {"answer" : answer }, 200

@app.route("/answer", methods=["POST"])
def answer():
    global context
    doc_txt = None
    if not os.path.isdir("database") or not os.listdir("database"):
        return {"answer" : "Pas de fichier mis en ligne"}, 200
    else:
        document = read_pdf("database/current_file.pdf")
        doc_txt = split_text(document)[0]
    answer = request.form["prompt"]
    context["human"+ str(len(context))] = [answer, True]
    gpt_validation = gpt3_completion(context_to_text(context, True), text = doc_txt)
    context["ai" + str(len(context))] = [gpt_validation, True]
    return {"answer" : gpt_validation }, 200
  
@app.route("/resetcontext")
def reset():
    try:
        for filename in os.listdir("database"):
            os.remove(f"database/{filename}")
    except:
        pass
    global context
    context = {}
    message = "Je suis ton AIssistant de cours personnel ! Pose-moi une question sur le cours et je te répondrai."
    return message
