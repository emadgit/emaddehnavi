from flask import Flask, jsonify

endpoint_url = "http://localhost.localstack.cloud:4566"

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify(message="Welcome to our API home!")


def start():
    msg = """
    Welcome to our API powered by Flask 👋
    In this API we showcase how to use 
    Localstack in your local machine!
    """
    print(msg)
    app.run()
