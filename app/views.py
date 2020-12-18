from app import app
from flask import render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
#import librosa
#from sklearn import preprocessing
#import python_speech_features as mfcc

dirname = os.path.dirname(__file__)
uploads_folder = os.path.join(dirname, 'static/uploads')
app.config["UPLOADS"] = uploads_folder
app.config["ALLOWED_EXTENSIONS"] = ["MP3", "WAV", ]


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.files:
            print(request.files)
            audio_file = request.files["audio_file"]

            if not isValidAudioFile(audio_file.filename):
                print("That file is not valid")
                return render_template('public/index.html', error="Please upload a valid file! Thanks.")

            filename = secure_filename(audio_file.filename)
            audio_file.save(os.path.join(app.config["UPLOADS"], filename))

        return render_template('public/index.html', filename=filename, input=[[3.49943221e-01,  1.78442045e+03,  2.00265019e+03,  3.80648532e+03,
                                                                               8.30663910e-02, -1.13596748e+02,  1.21557297e+02, -1.91588268e+01,
                                                                               4.23510284e+01, -6.37645817e+00,  1.86188755e+01, -1.36979122e+01,
                                                                               1.53446312e+01, -1.22852669e+01,  1.09804916e+01, -8.32432461e+00,
                                                                               8.81066894e+00, -3.66736817e+00,  5.75169086e+00, -5.16276264e+00,
                                                                               7.50947773e-01, -1.69193780e+00, -4.09952581e-01, -2.30020881e+00,
                                                                               1.21992850e+00]])

    return render_template("public/index.html")

def isValidAudioFile(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False
