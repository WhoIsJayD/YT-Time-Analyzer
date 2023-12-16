from datetime import datetime, timedelta
import json
import os
import re
import requests
from flask import Flask, Response, request, render_template
import isodate
from flask_cors import CORS
from talisman import Talisman

MAX_RESULTS_PER_PAGE = 50
MAX_VIDEOS_LIMIT = 500
MAX_TIME_SLICE = 10

# Set your secret key
SECRET_KEY = os.environ.get('SECRET')

# Set your API keys as environment variables
APIS = os.environ.get('APIS')

if not APIS:
    raise ValueError('APIS environment variable not set')

APIS = APIS.strip('][').split(',')

URL1 = 'https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={}&fields=items/contentDetails/videoId,nextPageToken&key={}&playlistId={}&pageToken='
URL2 = 'https://www.googleapis.com/youtube/v3/videos?&part=contentDetails&id={}&key={}&fields=items/contentDetails/duration'

app = Flask(__name__, static_url_path='/static')
app.secret_key = SECRET_KEY

# Enable CORS for all routes
CORS(app)

# Enable security headers
Talisman(app)

def get_id(playlist_link):
    p = re.compile('^([\S]+list=)?([\w_-]+)[\S]*$')
    m = p.match(playlist_link)
    return m.group(2) if m else 'invalid_playlist_link'

def parse_duration(a):
    ts, td = a.seconds, a.days
    th, tr = divmod(ts, 3600)
    tm, ts = divmod(tr, 60)
    ds = ''
    
    if td:
        ds += f' {td} day{"s" if td != 1 else ""},'
    if th:
        ds += f' {th} hour{"s" if th != 1 else ""},'
    if tm:
        ds += f' {tm} minute{"s" if tm != 1 else ""},'
    if ts:
        ds += f' {ts} second{"s" if ts != 1 else ""}'

    return ds.strip().strip(',') if ds else '0 seconds'

def today_at(hr, min=0, sec=0, micros=0):
    now = datetime.now()
    return now.replace(hour=hr, minute=min, second=sec, microsecond=micros)

def find_time_slice():
    time_slices = [0, 4, 8, 12, 16, 20, 22, 24]
    time_now = datetime.now()

    for i in range(len(time_slices) - 1):
        if today_at(time_slices[i]) <= time_now < today_at(time_slices[i + 1]):
            return i

    return MAX_TIME_SLICE

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template("home.html")
    else:
        playlist_link = request.form.get('search_string').strip()
        playlist_id = get_id(playlist_link)
        next_page = ''
        cnt = 0
        total_duration = timedelta(0)
        time_slice = find_time_slice()
        display_text = []

        while True:
            video_ids = []

            try:
                results = json.loads(requests.get(URL1.format(MAX_RESULTS_PER_PAGE, APIS[time_slice], playlist_id) + next_page).text)

                for item in results.get('items', []):
                    video_ids.append(item['contentDetails']['videoId'])

            except (KeyError, json.JSONDecodeError, requests.RequestException) as e:
                display_text = [f'Error: {e}']
                break

            url_list = ','.join(video_ids)
            cnt += len(video_ids)

            try:
                op = json.loads(requests.get(URL2.format(url_list, APIS[time_slice])).text)

                for item in op.get('items', []):
                    total_duration += isodate.parse_duration(item['contentDetails']['duration'])

            except (KeyError, json.JSONDecodeError, requests.RequestException) as e:
                display_text = [f'Error: {e}']
                break

            if 'nextPageToken' in results and cnt < MAX_VIDEOS_LIMIT:
                next_page = results['nextPageToken']
            else:
                if cnt >= MAX_VIDEOS_LIMIT:
                    display_text = ['No of videos limited to 500.']
                display_text += [
                    f'No of videos: {cnt}',
                    f'Average length of video: {parse_duration(total_duration / cnt)}',
                    f'Total length of playlist: {parse_duration(total_duration)}',
                ]

                for speed in [1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5]:
                    display_text.append(f'At {speed}x: {parse_duration(total_duration / speed)}')

                break

        return render_template("home.html", display_text=display_text)

@app.route("/healthz", methods=['GET', 'POST'])
def healthz():
    try:
        # Add any health check logic here
        return "Success", 200
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/.well-known/brave-rewards-verification.txt')
def static_from_root_brave():
    return Response(
        'This is a Brave Rewards publisher verification file.\n\nDomain: ytplaylist-len.herokuapp.com\nToken: aae68b8a5242a8e5f0505ee6eaa406bd51edf0dc9a05294be196495df223385c',
        mimetype='text/plain')

@app.route('/ads.txt')
def static_from_root_google():
    return Response(
        'google.com, pub-8874895270666721, DIRECT, f08c47fec0942fa0',
        mimetype='text/plain')

if __name__ == "__main__":
    app.run(use_reloader=True, debug=False)
