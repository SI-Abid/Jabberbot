import discord
import os
import requests
import json
from keep_alive import keep_alive
from replit import db

token = os.environ['TOKEN']
# ki holo
# list = []

bot = discord.Client()

def add_key(word):
  if 'greet' in db.keys():
    list = db['greet']
    if word not in list:
      list.append(word)
    db['greet'] = list
  else:
    db['greet'] = [word]


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

  msg = message.content.lower()

  if any (word in msg for word in db['greet']):
    await message.channel.send("Hello World\nWhat's up **{0.author.name}** :smile:".format(message))
  
  if msg.startswith('$inspire'):
    await message.channel.send(get_quote())

  if msg.startswith('$new'):
    words = msg.split(' ',1)[1].split(' ')
    for word in words:
      add_key(word)
    await message.channel.send('Database update\n{0}'.format(db['greet'].value))


keep_alive()
bot.run(token)


# list = ['hi', 'hlw', 'hello', 'hola']