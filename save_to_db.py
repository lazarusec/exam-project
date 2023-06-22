import praw
import mysql.connector
import datetime

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

cursor = conn.cursor()

create_table = """
    CREATE TABLE IF NOT EXISTS posts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        author VARCHAR(255),
        timestamp TIMESTAMP,
        score INT,
        url VARCHAR(2048)
    )"""

cursor.execute(create_table)

subreddit = reddit.subreddit("all")
for submission in subreddit.hot(limit=10):
    insert_query = """
        INSERT INTO posts (title, author, timestamp, score, url)
        VALUES (%s, %s, %s, %s, %s)"""
    
    utc_datetime = datetime.datetime.fromtimestamp(submission.created_utc)
    utc_string = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
    post_data = (submission.title, str(submission.author), utc_string, int(submission.score), submission.url)
    cursor.execute(insert_query, post_data)
    conn.commit()
conn.close()
