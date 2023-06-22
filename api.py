from fastapi import FastAPI
from fastapi.responses import JSONResponse
import praw
import datetime
import mysql.connector

app = FastAPI()

reddit = praw.Reddit(
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
    user_agent="Scrapper 1.0 by /u/lazarusec",
)

conn = mysql.connector.connect(
    host='localhost',
    user='username',
    password='password',
    database='db_name'
)

crawled_posts = []


@app.get('/api/posts')
async def get_posts():
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


@app.get('/api/db/posts')
async def get_db_posts():
    query = "SELECT * FROM posts"
    cursor.execute(query)
    datas = cursor.fetchall()
    return datas


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
