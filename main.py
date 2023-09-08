from flask import Flask, render_template, request
import os, atexit, json
from src.utils.ask_question_to_pdf import gpt3_completion, split_text, read_pdf

app = Flask(__name__)


default_message = "Je suis ton AIssistant de cours personnel ! Pose-moi une question sur le cours et je te répondrai."
context = {}

if os.path.exists("context.json"):
    with open("context.json", "r") as file:
        context = json.load(file)
else:
    context = {}


def save_context_to_json():
    with open("context.json", "w") as file:
        json.dump(context, file)


atexit.register(save_context_to_json)


def context_to_text(json_c, get_all=True):
    textual_c = ""
    for x in json_c:
        if get_all or json_c[x][1]:
            textual_c = textual_c + json_c[x][0] + "\n"

    return textual_c


def get_pdf_name():
    if not os.path.isdir("database") or not os.listdir("database"):
        return "Pas de fichier"
    else:
        return os.listdir("database")[0]


@app.route("/")
def hello_world():
    return render_template("index.html", filename=get_pdf_name(), context=context)


@app.route("/prompt", methods=["POST"])
def prompt():
    global context
    question = request.form["prompt"]
    doc_txt = None
    if not os.path.isdir("database") or not os.listdir("database"):
        pass
    else:
        filename = "database/" + os.listdir("database")[0]
        document = read_pdf(filename)
        doc_txt = split_text(document)[0]
    answer = gpt3_completion(context_to_text(context, True) + question, text=doc_txt)
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
    filepath = f"database/{file.filename}"
    file.save(filepath)
    return {"answer": "Le fichier a bien été mis en ligne. \n" + default_message}, 200


@app.route("/question", methods=["GET"])
def question():
    global context
    doc_txt = None
    if not os.path.isdir("database") or not os.listdir("database"):
        return {"answer": "Pas de fichier mis en ligne"}, 200
    else:
        filename = "database/" + os.listdir("database")[0]
        document = read_pdf(filename)
        doc_txt = split_text(document)[0]
    context["human" + str(len(context))] = [
        "Peux tu me poser une question sur ce texte ?",
        False,
    ]
    answer = gpt3_completion(context_to_text(context, True), text=doc_txt)
    context["ai" + str(len(context))] = [answer, True]
    return {"answer": answer}, 200


@app.route("/answer", methods=["POST"])
def answer():
    global context
    doc_txt = None
    if not os.path.isdir("database") or not os.listdir("database"):
        return {"answer": "Pas de fichier mis en ligne"}, 200
    else:
        filename = "database/" + os.listdir("database")[0]
        document = read_pdf(filename)
        doc_txt = split_text(document)[0]
    answer = request.form["prompt"]
    context["human" + str(len(context))] = [answer, True]
    gpt_validation = gpt3_completion(context_to_text(context, True), text=doc_txt)
    context["ai" + str(len(context))] = [gpt_validation, True]
    return {"answer": gpt_validation}, 200


@app.route("/resetcontext")
def reset():
    try:
        for filename in os.listdir("database"):
            os.remove(f"database/{filename}")
    except:
        pass
    global context
    context = {}
    message = default_message
    return message
