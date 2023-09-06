from flask import Flask, render_template, request
from src.utils.ask_question_to_pdf import gpt3_completion


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
    return {"answer": answer}, 200


# test
