from flask import Flask, render_template_string, request, redirect, url_for
from collections import Counter

app = Flask(__name__)

# Database maathiri temporary storage
polls = {
    1: {
        "question": "Which programming language do you like most?",
        "options": ["Python", "Java", "JavaScript", "C++"],
        "votes": []
    }
}
poll_id_counter = 2

# HTML + CSS ellam intha single file la irukku da, easy ah
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Online Poll & Survey System</title>
<style>
body{font-family:Arial; background:#f4f6f9; padding:20px}
.card{background:white; padding:20px; border-radius:10px; margin-bottom:20px; box-shadow:0 2px 5px #ccc}
button{background:#0d6efd; color:white; border:none; padding:8px 15px; border-radius:5px; cursor:pointer}
.progress{height:20px; background:#e9ecef; border-radius:10px; overflow:hidden; margin:5px 0}
.bar{height:100%; background:#0d6efd}
</style>
</head>
<body>
<h2>📊 Online Poll & Survey System - Priyadharshini</h2>

<div class="card">
<h3>Create New Poll / Survey</h3>
<form method="post" action="/create">
<input type="text" name="question" placeholder="Enter Question" required style="width:70%; padding:8px">
<input type="text" name="options" placeholder="Options comma separated Ex: Yes,No,Maybe" required style="width:70%; padding:8px; margin-top:10px">
<br><br><button type="submit">Create Poll</button>
</form>
</div>

{% for id, poll in polls.items() %}
<div class="card">
<h3>Q{{id}}: {{poll.question}}</h3>
<form method="post" action="/vote/{{id}}">
{% for opt in poll.options %}
<input type="radio" name="option" value="{{opt}}" required> {{opt}}<br>
{% endfor %}
<br><button type="submit">Vote</button>
</form>

<h4>Analytics & Reporting:</h4>
<p>Total Votes: {{poll.votes|length}}</p>
{% set count = poll.counter %}
{% for opt in poll.options %}
{{opt}} - {{count[opt]}} votes
<div class="progress"><div class="bar" style="width:{{ (count[opt]/poll.votes|length*100) if poll.votes else 0 }}%"></div></div>
{% endfor %}
</div>
{% endfor %}
</body>
</html>
"""

@app.route("/")
def home():
    for p in polls.values():
        p["counter"] = Counter(p["votes"])
    return render_template_string(HTML_TEMPLATE, polls=polls)

@app.route("/create", methods=["POST"])
def create():
    global poll_id_counter
    q = request.form["question"]
    opts = [o.strip() for o in request.form["options"].split(",") if o.strip()]
    polls[poll_id_counter] = {"question": q, "options": opts, "votes": []}
    poll_id_counter += 1
    return redirect("/")

@app.route("/vote/<int:pid>", methods=["POST"])
def vote(pid):
    opt = request.form["option"]
    polls[pid]["votes"].append(opt)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)