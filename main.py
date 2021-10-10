import discord
import os
import requests
import json
from keep_alive import keep_alive
from replit import db

bot = discord.Client()

token = os.environ['TOKEN']
prefix = '$'
# ki holo
# list = []

if 'responding' not in db.keys():
  db['responding'] = True

def add_key(word):
  if 'greet' in db.keys():
    list = db['greet']
    if word not in list:
      list.append(word)
    db['greet'] = list
  else:
    db['greet'] = [word]

def del_key(idx):
  list = db['greet']
  if len(list) > idx:
    del list[idx]
    db['greet'] = list


def get_quote():
  res = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(res.text)
  quote = json_data[0]['q'] + " -*" + json_data[0]['a'] + '*'
  return quote


@bot.event
async def on_ready():
  print('Hello I am online')# me too
  print('Connected as {0.user}'.format(bot))


@bot.event
async def on_message(message):

  if message.author == bot.user:
    return

  if not message.content.startswith(prefix):
    return

  msg = message.content.lower()[1:]

  if db['responding'] and any (word in msg for word in db['greet']):
    await message.channel.send("Hello World\nWhat's up **{0.author.name}** :smile:".format(message))
  
  if msg.startswith('inspire'):
    await message.channel.send(get_quote())

  if msg.startswith('new'):
    words = msg.split(' ',1)[1].split(' ')
    for word in words:
      add_key(word)
    await message.channel.send('Database updated\n{0}'.format(db['greet'].value))

  if msg.startswith('del'):
    list = []
    if 'greet' in db.keys():
      idx = int(msg.split(' ')[1])
      del_key(idx-1)
      list = db['greet']
    await message.channel.send('Database updated\n'+list.value)

  if msg.startswith('respond'):
    value = msg.split(' ',1)

    if len(value)>1 and value[1] == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")
    

keep_alive()
bot.run(token)


# list = ['hi', 'hlw', 'hello', 'hola']