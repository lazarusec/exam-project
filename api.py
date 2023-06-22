from flask import Flask
import praw
import datetime
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

reddit = praw.Reddit(
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
    user_agent="Scrapper 1.0 by /u/lazarusec",)

conn = mysql.connector.connect(
    host='localhost',
    user='username',
    password='password',
    database='db_name'
)

crawled_posts = []

@app.route('/api/posts')
def get_posts():
    subreddit = reddit.subreddit('all')
    crawled_posts.clear()
    for post in subreddit.new(limit=10):
        
        utc_datetime = datetime.datetime.fromtimestamp(post.created_utc)
        utc_string = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
        crawled_posts.append({
            'title': post.title,
            'author': post.author.name,
            'timestamp': utc_string
        })
    return crawled_posts

cursor = conn.cursor()

@app.route('/api/db/posts')
def get_db_posts():
    query = "SELECT * FROM posts"
    cursor.execute(query)
    datas = cursor.fetchall()
    return datas


if __name__ == '__main__':
    app.run(debug=True)


