#!/usr/bin/python

import praw
import bot
import time
import sqlite3
from pprint import pprint
import reversegif
import paths

SQL_CommentTableCreate = 'CREATE TABLE IF NOT EXISTS comments(ID TEXT)'
SQL_PostTableCreate = 'CREATE TABLE IF NOT EXISTS posts(ID TEXT, URL TEXT)'
SQL_CommentSearch = 'SELECT * FROM comments WHERE ID=?'
SQL_PostSearch = 'SELECT * FROM posts WHERE ID=?'
SQL_CommentInsert = 'INSERT INTO comments VALUES(?)'
SQL_PostInsert = 'INSERT INTO posts VALUES(?,?)'

REPLY_GIF_TOO_LARGE = 'Sorry, this gif is too large for me to upload to Imgur.'
KEYWORDS = ['reverse please', 'reverse plz', 'reversebot: reverse', 'gifbot: reverse']
MAX_POSTS = 200
WAIT_SEC = 30
SUBREDDIT = 'Gifs'

user_name = bot.get_username()
password = bot.get_password()
user_agent = bot.get_useragent()

sql = sqlite3.connect(paths.db_file('sql.db'))
print('Loaded SQL Database')

cursor = sql.cursor()
cursor.execute(SQL_CommentTableCreate)
cursor.execute(SQL_PostTableCreate)
print('oldposts Table loaded')

sql.commit()

r = praw.Reddit(user_agent)
r.login(user_name, password)

def get_reply_string(gif_url):
    return 'Reversed for your viewing pleasure: ' + gif_url

def scanSub():
    print 'searching ' + SUBREDDIT
    sub = r.get_subreddit(SUBREDDIT)
    comments = sub.get_comments(limit=MAX_POSTS)
    for comment in comments:
        comment_id = comment.id
        post_id = comment.link_id[3:len(comment.link_id)]
        gif_url = comment.link_url

        #pprint(vars(post))

        try:
            author = comment.author.name
        except AttributeError:
            author = '[DELETED]'

        cursor.execute(SQL_CommentSearch, [comment_id])

        if not cursor.fetchone():
            cursor.execute(SQL_CommentInsert, [comment_id])
            body = comment.body.lower()

            if any(key.lower() in body for key in KEYWORDS):
                if author != user_name:
                    cursor.execute(SQL_PostSearch, [post_id])
                    post = cursor.fetchone()
                    reversed_gif_url = ''
                    try:
                        if not post:
                            print 'post not cached'
                            reversed_gif_url = reversegif.do_reverse(gif_url)

                            print 'caching post:', post_id, reversed_gif_url
                            cursor.execute(SQL_PostInsert, [post_id, reversed_gif_url])
                        else:
                            print 'cached post found!'
                            reversed_gif_url = post[1]

                        reply_text = get_reply_string(reversed_gif_url)
                        print reply_text
                        comment.reply(reply_text)
                    except reversegif.ImageSizeException as e:
                        print e
                        comment.reply(REPLY_GIF_TOO_LARGE)
                    except reversegif.SmileyPostException as s:
                        print s
                    except Exception as ex:
                        print 'Exception occured while reversing!'
                        print ex
                else:
                    print '___ DO NOT REPLY TO SELF ___'

    sql.commit()

while True:
    try:
        scanSub()
    except Exception as e:
        print 'an error occurred:'
        print e
    print 'Running again in', WAIT_SEC, 'seconds\n'
    sql.commit()
    time.sleep(WAIT_SEC)
