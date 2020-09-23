from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def index():
    message = request.form.get("message_input")
    print(message)
    return render_template('index.html', message=message)

if __name__ == "__main__":
    app.run()
