from app import app
from flask import render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import librosa
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from pickle import load
#from sklearn import preprocessing
#import python_speech_features as mfcc

dirname = os.path.dirname(__file__)
uploads_folder = os.path.join(dirname, 'static/uploads')
app.config["UPLOADS"] = uploads_folder
app.config["ALLOWED_EXTENSIONS"] = ["MP3", "WAV", ]

# define min max scaler
scaler = load(open(os.path.join(dirname, 'static/scaler.pkl'), 'rb'))

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            if request.files:
                print(request.files)
                audio_file = request.files["audio_file"]

                if not isValidAudioFile(audio_file.filename):
                    print("That file is not valid")
                    return render_template('public/index.html', error="Please upload a valid file! Thanks.")

                filename = secure_filename(audio_file.filename)
                audio_file.save(os.path.join(app.config["UPLOADS"], filename))

                file_path = os.path.join(app.config["UPLOADS"], filename)
                
                features = extractFeatures(file_path).tolist()

                return render_template('public/index.html', filename=filename, input=features)

            return render_template('public/index.html', error="Please upload a valid file! Thanks.")

        except:
            return render_template('public/index.html', error="Error processing your file.")

    return render_template("public/index.html")

def isValidAudioFile(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False

def extractFeatures(filename):
    songname = filename
    y, sr = librosa.load(songname, mono=True, duration=30)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rmse = librosa.feature.rms(y=y)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    to_append = f'{np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'    
    for e in mfcc:
        to_append += f' {np.mean(e)}'
    
    features = to_append.split()
    del features[1]

    features_array = np.array([features])

    # transform data
    scaled = scaler.transform(features_array)

    return scaled.astype(np.double)