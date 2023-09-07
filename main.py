from flask import Flask, render_template, request, redirect
import os
from src.utils.ask_question_to_pdf import gpt3_completion, split_text, read_pdf


app = Flask(__name__)

context = ""


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/prompt", methods=["POST"])
def prompt():
    global context
    question = request.form["prompt"]
    answer = gpt3_completion(context + "\n" + question)
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
    filepath = "database/current_file.pdf"
    file.save(filepath)

    document = read_pdf(filepath)
    chunks = split_text(document)

    return redirect("/")

@app.route("/question", methods=["GET"])
def question():
    global context
    doc_txt = None
    if not os.listdir("database"):
        return {"answer" : "Pas de fichier mis en ligne"}, 200
    else:
        document = read_pdf("database/current_file.pdf")
        doc_txt = split_text(document)[0]
    context = context + "\n" + "Peux tu me poser une question sur ce texte ?"
    answer = gpt3_completion(context, text = doc_txt)
    context = context + "\n" + answer
    print(answer)
    return {"answer" : answer }, 200

@app.route("/answer", methods=["POST"])
def answer():
    global context
    doc_txt = None
    if not os.listdir("database"):
        return {"answer" : "Pas de fichier mis en ligne"}, 200
    else:
        document = read_pdf("database/current_file.pdf")
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
    message = "test"
    return message
