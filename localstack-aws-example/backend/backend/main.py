from flask import Flask, jsonify, request, send_file
from flask_cors import cross_origin
import boto3
from werkzeug.utils import secure_filename
from backend import S3_BUCKET, LOCAL_STACK_ENDPOINT

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify(message="Welcome to our API home!")


@app.route("/upload", methods=["POST"])
@cross_origin(["*"])
def upload():
    try:
        print("request.files", request.files)
        if "MyFile" not in request.files:
            return jsonify(message="No file part"), 400
        file = request.files["MyFile"]
        filename = secure_filename(file.filename)
        client = boto3.client("s3", endpoint_url=LOCAL_STACK_ENDPOINT)
        client.put_object(Bucket=S3_BUCKET, Key="uploads/" + filename, Body=file)
        return jsonify(message="File uploaded successfully to S3 bucket"), 200
    except Exception as err:
        print(f"Something went wrong. {err}")


@app.route("/download/<key>")
@cross_origin(["*"])
def download(key):
    try:
        print(f"Downloading {key} from S3 {S3_BUCKET} bucket")
        client = boto3.client("s3", endpoint_url=LOCAL_STACK_ENDPOINT)
        my_file = client.get_object(Bucket=S3_BUCKET, Key="uploads/" + key)
        return send_file(my_file["Body"], download_name=key)
    except Exception as err:
        print(f"Something went wrong. {err}")


def start():
    msg = """
    Welcome to our API powered by Flask 👋
    In this API we showcase how to use 
    Localstack in your local machine!
    """
    print(msg)
    app.run()
