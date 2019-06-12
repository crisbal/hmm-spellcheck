from correct import correct, words
from flask import Flask, render_template, request, jsonify
app = Flask(__name__, static_folder="web_interface", template_folder="web_interface")

@app.route("/")
def hello():
  return render_template('index.html')

@app.route("/api/successors")
def successors():
  text = request.args.get("text","")
  if text == "":
    return jsonify(
      sorted(words["START_SENTENCE"].keys(), key=lambda x: words["START_SENTENCE"][x], reverse=True)
    )

  return "none"

app.run(debug=True)
