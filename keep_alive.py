from flask import Flask, render_template
from threading import Thread
from replit import db

app = Flask('')

@app.route('/')
def home():
  return "Hello, I am alive"

@app.route('/index')
def index():
  user = {'username': 'User'}
  posts = [
    {
      'author': {'username': 'Saiham'},
      'body': 'First post in this page!'
    }
  ]
  if 'posts' in db.keys():
    for post in db['posts']:
      posts.append(post)

  return render_template('index.html', title='Home', user=user, posts=posts)


def run():
  app.run(host="0.0.0.0", port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()

