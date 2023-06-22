from flask import Flask, render_template
from flask_socketio import SocketIO
import praw
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

reddit = praw.Reddit(
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
    user_agent="Scrapper 1.0 by /u/lazarusec",)

live_updates = [] 

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    send_live_updates()

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/')
def index():
    return render_template('dashboard.html')

def send_live_updates():
    subreddit = reddit.subreddit('all')

    live_updates.clear()
    
    for post in subreddit.new(limit=10):
        utc_datetime = datetime.datetime.fromtimestamp(post.created_utc)
        utc_string = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
        live_updates.append({
            'title': post.title,
            'author': post.author.name,
            'timestamp': utc_string,
            'url': post.url
        })

    socketio.emit('live_updates', live_updates)

if __name__ == '__main__':
    socketio.run(app, debug=True)


