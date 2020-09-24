from flask import Flask, render_template, request

app = Flask(__name__)

messages = []

@app.route('/', methods=["POST", "GET"])
def index():
    global messages 
    message = request.form.get("message_input")
    messages.append(message)
    print(messages)
    print(message)
    
    return render_template('index.html', message = messages)

if __name__ == "__main__":
    app.run()
