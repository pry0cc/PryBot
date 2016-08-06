#!/usr/bin/env python2

from creds import Creds
import urllib2
from bs4 import BeautifulSoup
import Legobot
import subprocess
import time
from pydiscourse.client import DiscourseClient

creds = Creds()
HOST = creds.HOST
PORT = creds.PORT
NICK = creds.NICK
PASS = creds.PASS
CHANS = creds.CHANS

myBot = Legobot.legoBot(host=HOST,port=PORT,nick=NICK,nickpass=PASS,chans=CHANS)
client = DiscourseClient('https://0x00sec.org', api_username='localhost', api_key=creds.API_KEY)

# def latestTopics(msg):
#     p = subprocess.Popen('ruby discourse.rb latest', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     return p.stdout.readlines()
# def topic(msg):
#     p = subprocess.Popen('ruby discourse.rb topic ' + msg.arg1 + ' ' + msg.actualUserName, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     return p.stdout.readlines()

def UrlFromID(id):
  data = client.topic_posts(id)["post_stream"]["posts"][0]
  return "https://0x00sec.org/t/%s/%s" % (data["topic_slug"], data["topic_id"])

def join(msg):
    myBot.sendMsg("JOIN " + msg.arg1 + "\r\n")

def whois(msg):
    username = msg.arg1
    print "Searching " + username
    data = client.user(username)
    bio = ""
    website = ""
    location = ""

    if "bio_raw" in data:
      bio = data["bio_raw"].split("\n")[0]

    if "website" in data:
      website = data["website"]

    if "location" in data:
      location = data["location"]

    output_str = ""

    if (bio and website and location):
      output_str = username + " is a " + bio + " from " + location + ". He/She also has a website at " + website
    elif (bio and website and (location == "")):
      output_str = username = " is a " + bio + ". He/She also has a website at " + website
    elif (bio and location and (website == "")):
      output_str = username + " is a " + bio + ". He/She is from " + location
    elif (bio and (location == "") and (website == "")):
      output_str = username + " is a " + bio
    else:
        if (bio == ""):
            output_str = username + " is boring and has not supplied any info xD"
        else:
            output_str = "I don't know.. Something happened?"
    return output_str

def topic(msg):
    return UrlFromID(msg.arg1)

def latest(msg):
    data = client.latest_topics()["topic_list"]["topics"]
    output = []

    for topic in data[0:5]:
        output.append(str(topic["id"]) + " " + topic["title"])

    return output

def wiki_search(msg):
    import requests
    if not msg.arg1:
      return "Wikipedia Top Finder. Search English Wikipedia for an article. Usage: !wtf [query]"
    baseurl = 'https://en.wikipedia.org/w/index.php?search='
    search_params = '%20'.join(msg.splitMessage[4:])
    r = requests.get(baseurl+search_params)
    if r.status_code == 200:
        return "I found this: " + r.url
    else:
        return "I could not reach Wikipedia. Sorry."
myBot.setThrottle(0.5)
# myBot.addFunc("!latest", latestTopics, "Ask your bot to say hello. Usage: !helloworld")
# myBot.addFunc("!topic", topic, "Ask your bot to say hello. Usage: !helloworld")
myBot.addFunc("!join", join, "Be a total bitch and annoy other channels. Usage: !join #channel")
myBot.addFunc("!whois", whois, "Find out who somebody is on 0x00sec.org! Usage !whois username")
myBot.addFunc("!topic", topic, "Get the URL of a topic. Usage !topic 882")
myBot.addFunc("!latest", latest, "Get a list of the Latest Posts on 0x00sec. Usage !latest")
myBot.addFunc("!wtf", wiki_search, "Search Wikipedia. Usage !wtf search")


myBot.connect(isSSL=False)
