from fastapi import FastAPI
from datetime import datetime
import os

if not os.path.exists('chat.txt'):
    open('chat.txt', 'w').close()

app = FastAPI()


@app.get("/")
def read_root():
    return 'ACTIVE AT '+ str(datetime.now())

@app.get("/allchat")
def allchat():
    return open('chat.txt', 'r', encoding='utf-8').read()

@app.post("/sendmsg/{from_who}/{msg}")
def sendmsg(from_who, msg):
    date_time=str(datetime.now())
    open('chat.txt', 'a', encoding='utf-8').write(f'\n[{from_who} at {date_time}] - {msg}\n')
    return 'Done'
