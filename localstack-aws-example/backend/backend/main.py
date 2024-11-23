from flask import Flask, jsonify, request
import boto3
from werkzeug.utils import secure_filename

endpoint_url = "http://localhost:4566/"

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify(message="Welcome to our API home!")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    try:
        if request.method == "POST":
            print("request.files", request.files)
            if "MyFile" not in request.files:
                return jsonify(message="No file part"), 400
            file = request.files["MyFile"]
            filename = secure_filename(file.filename)
            client = boto3.client("s3", endpoint_url=endpoint_url)
            client.put_object(
                Bucket="localstack-demo", Key="uploads/" + filename, Body=file
            )
    except:
        print("Something went wrong")
    else:
        return jsonify(message="File uploaded successfully to S3 bucket"), 200


def start():
    msg = """
    Welcome to our API powered by Flask 👋
    In this API we showcase how to use 
    Localstack in your local machine!
    """
    print(msg)
    app.run()
