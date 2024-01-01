from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pymongo
import logging
import pandas as pd
import json
import re

logging.basicConfig(filename="youtube_scrapper.log" , level=logging.INFO)

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/video" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        try:
            channel_url = 'https://www.youtube.com/@PW-Foundation/videos'
            # Send a GET request to the YouTube channel URL
            response = requests.get(channel_url)
            if response.status_code == 200:
                match = re.search(r'var\s+ytInitialData\s*=\s*({.*?});', response.text, re.DOTALL)
                yt_initial_data_json = match.group(1)
                yt_initial_data = json.loads(yt_initial_data_json)
                channel_details_list = [] 
            for i in range(5):
                details = {
                'VideoName': yt_initial_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']['richGridRenderer']['contents'][i]['richItemRenderer']['content']['videoRenderer']['title']['runs'][0]['text'],
                'VideoLink': 'https://www.youtube.com' + yt_initial_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']['richGridRenderer']['contents'][i]['richItemRenderer']['content']['videoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url'],
                'VideoThumnail': yt_initial_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']['richGridRenderer']['contents'][i]['richItemRenderer']['content']['videoRenderer']['thumbnail']['thumbnails'][3]['url'],
                'VideoTimeOfPost': yt_initial_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']['richGridRenderer']['contents'][i]['richItemRenderer']['content']['videoRenderer']['publishedTimeText']['simpleText'],
                'VideoViews': yt_initial_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']['richGridRenderer']['contents'][i]['richItemRenderer']['content']['videoRenderer']['viewCountText']['simpleText']
                }
                channel_details_list.append(details)
            df = pd.DataFrame(channel_details_list)
            return render_template('result.html', reviews=df)
        except Exception as e:
            logging.info(e)
            return 'something is wrong'
# return render_template('results.html')

    else:
        return render_template('index.html')



# if __name__ =='__main__':
#     app.run(host='0.0.0.0')
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)