import discord
import os
from server import keep_alive
from replit import db
from utils import *

bot = discord.Client()

token = os.environ['TOKEN2']
prefix = ';'
bin_link = 'http://scratch.si_abid.repl.co/bin'
# ki holo
# list = []

if 'responding' not in db.keys():
  db['responding'] = True



@bot.event
async def on_ready():
  print('Hello I am online')# me too
  print('Connected as {0.user}'.format(bot))


@bot.event
async def on_message(message):

  if message.author == bot.user:
    return

  msg = message.content.lower()[1:]
  
  if db['responding'] and any (word in message.content.split(' ') for word in db['greet']):
    await message.channel.send("Hello World\nWhat's up **{0.author.name}** :smile:".format(message))
  
  print(message.content)

  if not message.content.startswith(prefix):
    return
  
  if msg.startswith('inspire'):
    await message.channel.send(get_quote())

  if msg.startswith('new'):
    words = msg.split(' ',1)[1].split(' ')
    # for word in words:
    #   add_key(word)
    if len(words) >= 1:
      add_db('greet',words)
      await message.channel.send('Database updated\n{0}'.format(db['greet'].value))
    else:
      await message.channel.send('Not enough arguments.')

  if msg.startswith('del'):
    list = []
    if 'greet' in db.keys():
      idx = int(msg.split(' ')[1])
      del_key(idx-1)
      list = db['greet']
    await message.channel.send('Database updated\n{0}'.format(list.value))

  if msg.startswith('respond'):
    value = msg.split(' ',1)

    if len(value)>1 and (value[1] == "true" or value[1] == "on"):
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")
  
  if msg.startswith('cfup'):
    arg = msg.split(' ')
    day = 5
    if len(arg) > 1:
      day = int(arg[1])
    roles = ':calendar:'
    if 'pingable' in db.keys():
      for role in db['pingable']:
        roles+=' '+role
    await message.channel.send(roles)
    await message.channel.send('**{0.author.name}** requested **Codeforces update**'.format(message))
    for block in cfupdate(day):
      await message.channel.send('```'+block+'```')

  if msg.startswith('add'):
    args = msg.split(' ')
    if len(args) < 3:
      await message.channel.send('Invalid format\n*$add <key> [<value1> <value2> ...]*')
    else:
      key = args[1]
      values = args[2:]
      add_db(key,values)
      await message.channel.send('Database updated by **{0.author.name}**'.format(message))

  if msg.startswith('run'):
    args = message.content.split('```')
    # print(len(args))
    # for each in args:
    #   print("*"+each+"#")
    lang = args[0].split(' ')[1].lower()[:-1] #exclude tailing newline
    if len(args) < 2:
      # send reaction
      await message.channel.send('**Pardon me. What do you intend to run**')
    code , data = args[1], ""
    if len(args) >= 4:
      data = args[3][1:-1] # exclude leading and tailing newline
    # for i in range(len(args)):
    #   print(i,args[i])
    # print(lang,code,data)
    res = coderun(lang,code,data)
    if type(res) == str:
      await message.channel.send('`'+res+'`')
    else:
      out, mem, sec = res
      if len(out)>1999:
        await message.channel.send('**The output of you code is too big.**\nPlease use the broswer mode at {}'.format(bin_link))
      await message.channel.send('`Memory: {1}byte\t\tTime: {2}s`\n{0}'.format(mdstr(out),mem,sec))

  if msg.startswith('todo'):
    args = msg.split('\n')
    user = str(message.author)
    cmd = ''
    try:
      cmd = args[0].split(' ')[1]
    except:
      await message.channel.send(show_list(user))
  
    if len(args) == 1:
      #show list
      # print(user,type(user))
      if cmd == 'clear':
        del_list(user)
        await message.channel.send("**Your list has been cleared**")
      elif cmd == 'check':
        arg = args[0].split('check')
        if len(arg) < 2:
          await message.channel.send('**Too few arguments**')
        # [optional] check all
        else:
          for x in arg[1].split():
          # idx = int(arg[2])-1
            check_list(user,int(x)-1)
          await message.channel.send("**Checked**")
  
    else:
      if cmd == 'add':
        dolist = msg.split('\n')[1:] # excluding first line of input
        add_list(user,dolist)
        await message.channel.send("**Tasks added to you list**")

  if msg.startswith('send'):
    args = msg.split(' ')
    print(args[1], type(args[1]))
    person = message.mentions[0]
    text = msg.split(' ',2)[2]
    print(person)
    print(text)
    await person.send(text)

  # if msg.startswith('setp'):
  if msg.startswith('post'):
    try:
      ctx = message.content.split(';post ')[1]
      # print(ctx)
      if len(ctx) < 1:
        raise Exception('Not enough argument')
      post = {
        'author': {'username': message.author.name},
        'body': ctx
      }
      if 'posts' in db.keys():
        posts = db['posts']
        posts.append(post)
        db['posts']=posts
      else:
        db['posts']=[post]
      await message.channel.send("**Your post has been published**")
    except:
      await message.channel.send("**Invalid format**")



keep_alive()
bot.run(token)

# list = ['hi', 'hlw', 'hello', 'hola']