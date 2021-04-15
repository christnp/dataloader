import sys
import os
from flask import (Flask, render_template, 
                    request, flash, make_response,
                    redirect)
from werkzeug.utils import secure_filename
import random
from hashlib import sha1
from random import choice, randint
import requests
import json
from urllib.parse import urlparse, urlsplit

# usage:
# FLASK_ENV=development FLASK_APP=app.py flask run --port 5001


# Global constants
LOCALHOST = 'http://localhost:5000'
SRCDIR = os.path.dirname(os.path.abspath(__file__))
STATICDIR = 'static'
DATADIR = os.path.join(STATICDIR,'datasets')

# app = Flask(__name__, static_folder=SRCDIR)
app = Flask(__name__)


@app.route("/")
def index():
    # load last used address
    if os.path.isfile('server_address.txt'):
        with open('server_address.txt', 'r') as f:
            server_address = json.load(f)
        url = server_address['address']
        # pares_url = urlparse(url)
        address = url.rsplit('/', 1)[0]
        endpoint = url.rsplit('/', 1)[-1]
        # address = pares_url.netloc
        # endpoint = pares_url.path
    else:
        address = LOCALHOST
        endpoint = 'predict'
    
    # Load current count
    f = open("count.txt", "r")
    count = int(f.read())
    f.close()

    # Increment the count
    count += 1

    # Overwrite the count
    f = open("count.txt", "w")
    f.write(str(count))
    f.close()


    # we need to remove this so the images dynamically load
    for filename in os.listdir(DATADIR):
        if filename.startswith('source_'):  # not to remove other images
            os.remove(os.path.join(DATADIR,filename))

    # Render HTML with count variable
    return render_template("index.html", count=count,address=address,endpoint=endpoint)


@app.route("/results", methods=['POST'])
def results():
    # dataset to send
    # source_dataset = "../imagenet-sample-images/Blue_Jay_(210140531).JPEG"     
    # tmp_dir = os.path.join(SRCDIR,'static')
    dataset_path = 'static/datasets'
    if not os.path.isdir(dataset_path):
        os.mkdir(dataset_path)
    # 
    # target_address = "http://localhost:5000"
    # target_endpoint = "predict"
    if request.method == 'POST':
        source_dataset = request.files['dataset']
        target_address = request.form['address']
        target_endpoint = request.form['endpoint']

        if source_dataset.filename == '':
            flash('No selected file')   

        if not target_address:
            target_address = LOCALHOST

        source_name, source_ext = os.path.splitext(source_dataset.filename)
        #generate random version (to alleviate caching)
        source_version = '{:032}'.format(randint(0,10**31))
        source_cnt = '{:05}'.format(1)
        source_path = os.path.join(dataset_path,f'source_{source_cnt}'+source_ext)
        # source_path = os.path.join(dataset_path,f'{source_dataset.filename}?v={version}')

        source_dataset.save(source_path)

       

        # print(datasetname)
        url = f'{target_address}/{target_endpoint}'
        print("\n")
        print(target_address)
        print(target_endpoint)
        print(url)
        print("\n")
        resp = requests.post(url,
                        files={"file": open(source_path,'rb')})

       
        try:
            resp.json()
        except:
            err = f'ERROR: {sys.exc_info()[0]}'
            return render_template("index.html", error=err)

        # store the last used address for ease of use
        with open('server_address.txt', 'w') as f:
            json.dump({'address': url}, f, ensure_ascii=False)
        # render the html response
        rendering = make_response(render_template('results.html', 
                                dataset_version=source_version,
                                dataset_path=source_path, 
                                dataset_name=source_name,
                                class_name=resp.json()['class_name'], 
                                class_id=resp.json()['class_id']))
        # disable cache
        rendering.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        rendering.headers['Pragma'] = 'no-cache'
        return rendering
        # return render_template('results.html', dataset_path=source_path, 
        #                         dataset_name=source_name,
        #                         class_name=resp.json()['class_name'], 
        #                         class_id=resp.json()['class_id'])


# default cache settings (so we don't disable on all pages)
@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    if ('Cache-Control' not in response.headers):
        response.headers['Cache-Control'] = 'public, max-age=600'
    return response

if __name__ == "__main__":
    app.run(debug=True)