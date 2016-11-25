import sqlite3 as sqlite
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

json_str = urllib.request.urlopen("http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key=6a33b8fd34aeeea43f646ce5e887b996&format=json&limit=100").read().decode('utf-8')
loaded = json.loads(json_str)

list = []
count = 1
for x in loaded['artists']['artist']:
    list.append((x['name'], count, x['listeners'], x['playcount']))
    count = count + 1


with sqlite.connect(r'artist_popularity.db') as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS artists")
    cur.execute("CREATE TABLE artists (name VARCHAR(255), ID INTEGER, listeners INTEGER, playcount INTEGER);")
    cur.executemany("INSERT INTO artists VALUES (?, ?, ?, ?)", list)
    con.commit()
