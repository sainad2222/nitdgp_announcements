import telebot
import time
from bs4 import BeautifulSoup
import requests
import os
from replit import db
import hashlib
from keep_alive import keep_alive
from threading import Timer

Token = os.getenv('TOKEN')
myId = os.getenv('ID')
bot = telebot.TeleBot(token=Token)

def parse(takeurl):
  url = 'https://nitdgp.ac.in/p/notices-2/'+takeurl
  try:
    res = requests.get(url)
  except Exception as e:
    print(e)
  soup = BeautifulSoup(res.content,'html.parser')
  list_items = soup('a','list-group-item')
  conten = []
  for item in list_items:
      key = item.contents[1]
      val = item['href']
      encoded = key.encode('utf-8')
      hashed = hashlib.sha256(encoded).hexdigest()
      if hashed not in db:
        try:
          db[hashed] = val
        except Exception as e:
          print(key,val)
          print(e)
        conten.append(f"{key}  {val}")
  return conten

pages = ['general-2','academic-2','student-1','hostel','covid-19']

# contionus running function
def checker():
  for page in pages:
    results = parse(page)
    if results:
      try:
        bot.send_message(myId,'\n'.join(results))
      except Exception as e:
        print(e)
    else:
      bot.send_message(myId,"nothing")
    time.sleep(2)
  t = Timer(60*10, checker)
  t.daemon = True
  t.start()

checker()
keep_alive()

