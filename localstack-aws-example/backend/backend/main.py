from flask import Flask, jsonify, request
import boto3
from werkzeug.utils import secure_filename
from backend import S3_BUCKET

endpoint_url = "http://localhost:4566/"

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify(message="Welcome to our API home!")


@app.route("/upload", methods=["POST"])
def upload():
    try:
        print("request.files", request.files)
        if "MyFile" not in request.files:
            return jsonify(message="No file part"), 400
        file = request.files["MyFile"]
        filename = secure_filename(file.filename)
        client = boto3.client("s3", endpoint_url=endpoint_url)
        client.put_object(
            Bucket=variables.S3_BUCKET, Key="uploads/" + filename, Body=file
        )
        return jsonify(message="File uploaded successfully to S3 bucket"), 200
    except:
        print("Something went wrong")


@app.route("/download/<key>")
def download(key):
    try:
        print(f"Downloading {key} from S3 {S3_BUCKET} bucket")
        return jsonify(message="Successfull request."), 200
    except:
        print("Something went wrong")


def start():
    msg = """
    Welcome to our API powered by Flask 👋
    In this API we showcase how to use 
    Localstack in your local machine!
    """
    print(msg)
    app.run()
