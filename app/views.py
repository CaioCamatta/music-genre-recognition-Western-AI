from app import app
from flask import render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

@app.route('/')
def index():
    return render_template("public/index.html")

dirname = os.path.dirname(__file__)
uploads_folder = os.path.join(dirname, 'static/uploads')
app.config["UPLOADS"]= uploads_folder
app.config["ALLOWED_EXTENSIONS"]= ["MP3"]

def allowed_mp3(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/upload", methods=["GET", "POST"])
def upload_mp3():

    if request.method == "POST":

        if request.files:

            mp3 = request.files["mp3"]

            if mp3.filename == " ":
                print("File needs a name")
                return redirect(request.url)

            if not allowed_mp3(mp3.filename):
                print("That extension is not allowed")
                return redirect(request.url)

            else:
                filename = secure_filename(mp3.filename)

                mp3.save(os.path.join(app.config["UPLOADS"],filename))

            print("mp3 saved")

            return redirect(request.url)
            

    return render_template("public/upload_mp3.html")

