import requests
import json
from datetime import datetime
from replit import db
import os

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

def cfupdate(day):
  days = day*(-86400)
  res = requests.get("https://codeforces.com/api/contest.list?gym=false")
  results = json.loads(res.text)
  # print(results) # this is a dictionary
  ret = []
  for contest in results['result']: # each element is also a dictionary
    crts = contest['relativeTimeSeconds']
    if crts >= days and crts < 0:
      name = contest['name']
      if not name.isascii(): # if non-english name found
        continue
      starttime = datetime.fromtimestamp(contest['startTimeSeconds']+21600).strftime("Start: %a, %d %b %Y %r")
      lefttime = ''
      if crts >= -86400:
        lefttime = datetime.fromtimestamp(crts*(-1)).strftime("Time left: %H:%M:%S")
      else:
        lefttime = datetime.fromtimestamp(crts*(-1)-86400).strftime("Time left: %d days, %H:%M:%S")
      ret.append(name+'\n'+starttime+'\n'+lefttime)
  return ret

def add_db(key:str,values:list):
  if key in db.keys():
    value = db[key]
    for item in values:
      value.append(item)
    db[key]=value
  else:
    db[key] = values

def coderun(lang, code, data):
  program = {
    "script": code,
    "language": lang,
    "stdin": data,
    "versionIndex": "0",
    "clientId": os.environ['cID'],
    "clientSecret": os.environ['cSec']
  }

  res = requests.post(url="https://api.jdoodle.com/v1/execute",json=program)
  output = json.loads(res.text)
  # print(output)
  if output["statusCode"] == 200:
    obj = [output["output"],output["memory"],output["cpuTime"]]
    return obj
  else:
    return "Invalid language"

def show_list(user):
  li = "**"+user.split('#')[0]+"\'s todo list**\n```markdown\n"
  if user in db.keys():
    # print(db[user])
    for item in db[user]:
      li+=item+'\n'
    li+='```'
  else:
    li='```Your TODO list is empty```'
  return li

def check_list(user, idx:int):
  if user in db.keys():
    if idx < len(db[user]):
      if not db[user][idx].startswith('>'):
        db[user][idx] = '> '+db[user][idx]

def del_list(user):
  if user in db.keys():
    del db[user]

def add_list(user, tasks:list):
  todo = []
  if user in db.keys():
    todo = db[user]
  for task in tasks:
    if task not in todo:
      todo.append(str(len(todo)+1)+' '+task)
  db[user]=todo

def mdstr(s: str) -> str:
  return "```markdown\n"+s+"```"