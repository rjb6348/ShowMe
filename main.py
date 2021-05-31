from flask import Flask, render_template, request
import requests
from MusicLibrary import login
app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        if request.form.get('spotifylogin') == 'Login with Spotify':
            login() # do something
        elif  request.form.get('search') == 'Search':
            pass # do something else
        else:
            pass # unknown
    return render_template("index.html");
    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
