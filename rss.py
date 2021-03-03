import os
import pickledb # You can use any other database too. Use SQL if you are using Heroku Postgres.
import feedparser
from time import sleep, time
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from apscheduler.schedulers.background import BackgroundScheduler
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


# IL BOT DEVE ESSERE DENTRO IL TUO CANALE CON I PERMESSI


api_id = "0000000"   # ottieni il tuo api_id su my.telegram.org
api_hash = "00000000000000000000000000000000"   # ottieni il tuo api_hash su from my.telegram.org
feed_url = "https://www.ansa.it/sito/notizie/sport/calcio/calcio_rss.xml"   # link rss di ansa
bot_token = "0000000000000000000000000000000000000000000000"   # ottieni il bot token da https://t.me/botfather
log_channel = "@HyberNews"   # tag canale
check_interval = 3   # intervallo in secondi.  
max_instances = 3   # Max parallel instance to be used.

db = pickledb.load('rss.db', True)
if db.get("feed_url") == None:
  db.set("feed_url", "*")
app = Client("rss-bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

def check_feed():
    FEED = feedparser.parse(feed_url)
    entry = FEED.entries[0]
    if entry.id != db.get("feed_url"):

      
                   # ↓ edita il messaggio che pubblica sul canale.
      message = f"🔴 #Ultimora\n\n📰 **{entry.title}**\n\n🗞 {entry.summary}\n\n🔗<a href={entry.link}> Apri pagina</a>\n\n🔰 @HyberNews"
      

      try:
        app.send_message(log_channel, message)
        db.set("feed_url", entry.id)
      except FloodWait as e:
        print(f"FloodWait: {e.x} seconds")
        sleep(e.x)
      except Exception as e:
        print(e)
    else:
      print(f"Checked RSS FEED: {entry.id}")


scheduler = BackgroundScheduler()
scheduler.add_job(check_feed, "interval", seconds=check_interval, max_instances=max_instances)
scheduler.start()
app.run()
