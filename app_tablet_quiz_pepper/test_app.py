from flask import Flask
from flask import render_template, redirect, url_for, json, jsonify, request

# creates a Flask application, named app
app = Flask(__name__)

f = open('./static/questions.json', 'r')
quiz_data = f.read()
f.close()

# a route where we will display a welcome message via an HTML template
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data", methods=['GET', 'POST'])
def data():
    return jsonify(quiz_data) # convert your data to JSON and return

#### questionary-page ####
@app.route("/quiz", methods=['GET', 'POST'])
def quiz():
    # GET request
    #if request.method == 'GET':
    #    return jsonify(quiz_data)  # serialize and use JSON headers

    return render_template("quiz.html")

# run the application
if __name__ == "__main__":
    app.run(debug=True)
