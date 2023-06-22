from flask import Flask, render_template
from flask_socketio import SocketIO
import praw
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

reddit = praw.Reddit(
    client_id="xILKbnbYi-EdMu53o2F_Wg",
    client_secret="qCuiDM-WPkBztnO-JA2NImp2auQLfQ",
    user_agent="Scapper 1.o by /u/lazarusec",)

live_updates = []  # List to store live updates from Reddit

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
    # for post in subreddit.stream.submissions():
    #     utc_datetime = datetime.datetime.fromtimestamp(post.created_utc)
    #     utc_string = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
    #     live_updates.append({
    #         'title': post.title,
    #         'author': post.author.name,
    #         'timestamp': utc_string
    #     })
    
    for post in subreddit.new(limit=10):
        utc_datetime = datetime.datetime.fromtimestamp(post.created_utc)
        utc_string = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
        live_updates.append({
            'title': post.title,
            'author': post.author.name,
            'timestamp': utc_string
        })

    # Emit the live updates to connected clients
    socketio.emit('live_updates', live_updates)

if __name__ == '__main__':
    socketio.run(app, debug=True)


