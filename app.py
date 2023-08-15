"""Tiny app to serve the files in the Files directory."""
from flask import Flask, render_template, send_from_directory, request
from werkzeug.utils import secure_filename
from os import getcwd, walk, path, mkdir
from typing import Dict

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = getcwd() + "/Files"
app.config["ALLOWED_EXTENSIONS"] = {"zip", "rar", "7z", "tar", "gz", "xz", "bz2", "pdf", "txt", "docx", "doc", "xlsx", "xls", "pptx", "ppt", "png", "jpg", "jpeg", "gif", "mp4",
                                    "mp3", "flac", "ogg", "wav", "webm", "html", "css", "js", "json", "xml", "md", "gitignore", "gitattributes", "exe"}


@app.route('/')
def root():  # put application's code here
    files = scanDirectory()
    # Check if path exists

    return render_template("index.html", files=files)


@app.route('/<filePath>')
def serveFile(filePath: str):
    # Check if file exists
    if not path.exists(getcwd() + "/Files/" + filePath):
        return "File not found", 404

    return send_from_directory(getcwd() + "/Files", filePath)


def scanDirectory() -> Dict[str, Dict[str, str]]:
    """
    Scans the Files directory and returns a dictionary of the files. The items in the dictionary are dictionaries
    themselves with the keys 'filename' and 'downloadName'.
    """
    files = {}
    for root, dirs, filenames in walk(getcwd() + "/Files"):
        for filename in filenames:
            assert isinstance(filename, str)
            files[filename] = {'filename': filename.replace("_", " ").title(), 'downloadName': filename}

    return files


def allowed_file(filename: str) -> bool:
    """Checks if the file extension is allowed."""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


@app.route('/upload', methods=['POST'])
def uploadFile():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return "No selected file", 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
        return "File uploaded", 200

    return "File not allowed", 400


if __name__ == '__main__':
    # Ensure that the upload folder exists
    if not path.exists(app.config["UPLOAD_FOLDER"]):
        mkdir(app.config["UPLOAD_FOLDER"])

    if not path.exists(getcwd() + "/Files"):
        mkdir(getcwd() + "/Files")

    app.run()
