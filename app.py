from flask import Flask, request, render_template, redirect, flash
from random import randint, choice, sample
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES = []

app = Flask(__name__)
app.config["SECRET_KEY"] = "chickenzarecooll21837"

debug = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


@app.route("/")
def survey_start():
    qid = 0
    title = survey.title
    instructions = survey.instructions
    return render_template(
        "survey_start.html", title=title, instructions=instructions, qid=qid
    )


@app.route("/questions/<int:qid>", methods=["POST", "GET"])
def show_question(qid):
    qid = len(RESPONSES)
    current_url = request.url[-1::]
    if int(current_url) != qid:
        flash("Please stop trying to fucking access questions out of order, Karen")
        return redirect(f"/questions/{qid}")
    if qid >= len(survey.questions):
        return redirect("/thanks")
    question = survey.questions[qid]
    return render_template(
        "questions.html", question=question, qid=qid, current_url=current_url
    )


@app.route("/answer", methods=["POST"])
def pass_answer():
    qid = len(RESPONSES)
    response = request.form["answer"]
    RESPONSES.append(response)
    qid += 1
    return redirect(f"/questions/{qid}")


@app.route("/thanks")
def show_thanks():
    return render_template("thanks.html", RESPONSES=RESPONSES)
