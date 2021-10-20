from flask import Flask, render_template, redirect, request
from threading import Thread
from replit import db
from uuid import uuid4
from utils import coderun

URL = "http://scratch.si_abid.repl.co/bin"

app = Flask('')
app.config['SECRET_KEY'] = 'you-will-never-guess'

@app.route('/')
def home():
  return "Hello, I am alive"

@app.route('/index')
def index():
  posts = [
    {
      'author': {'username': 'Saiham'},
      'body': 'First post in this page!'
    }
  ]
  if 'posts' in db.keys():
    for post in db['posts']:
      posts.append(post)

  return render_template('index.html', title='Home', posts=posts)

@app.route('/bin', methods=['GET','POST'])
def bin():
  if request.method=='POST':
    user, code, lang, ptype, data = request.form['poster'], request.form['code'], request.form['syntax'], request.form['post_type'], request.form['data']
    if ptype == 'run':
      res = coderun(lang, code, data)[0]
      if type(res)==str:
        return render_template('mybin.html',user=user, code=code, output=res)
      else:
        return render_template('mybin.html',user=user, code='\n'.join(res))
    filename=uuid4().hex
    with open("./public/"+filename+'.txt',"w") as f:
      f.write(user)
      f.write('\n')
      f.write(code)
      return redirect('/mybin/'+filename)
  return render_template('bin.html')

@app.route('/mybin/<name>')
def mybin(name):
  loc='./public/'+name+'.txt'
  file = open(loc,"r")
  content = file.read()
  user, code = content.split('\n',1)
  return render_template('mybin.html',user=user, code=code)


def run():
  app.run(host="0.0.0.0", port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()
