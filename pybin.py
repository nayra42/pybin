#!/usr/bin/python3

"""
written by Ryan Coryell
designed to scrape pastebin for interesting stuff use regex to define what you want to look for run this as a service in system d for constant run in the background.  
You will need a pastebin pro account to use this script.
"""
import re
import requests
import time
import json
import urllib
import os
import smtplib
import logging
import datetime

##LOGING CONFIG BLOCK
#make a filelogger
filelogger = logging.getLogger(__name__)
#set logging level - debugging
#filelogger.setLevel(logging.DEBUG)
#set logging level - info
filelogger.setLevel(logging.INFO)
#setup handler
filelogger_handler = logging.FileHandler("/opt/pybin/python/pybin/pybin.log")
#format logs
filelogger_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
# Apply the formatter to the handler
filelogger_handler.setFormatter(filelogger_format)
# Apply the handler to the logger
filelogger.addHandler(filelogger_handler)

while True:
    try:

#def latest_pastes():
#this is the url to append the key to to get the raw paste
        rawPasteURL = 'https://scrape.pastebin.com/api_scrape_item.php?i='
#this is the url to grab keys, note a limit can be set with ?limit=x
        binInput = requests.get('https://scrape.pastebin.com/api_scraping.php?limit=100')
        filelogger.debug(binInput)
        filelogger.debug(dir(binInput))
        filelogger.debug(binInput.text)
        #input()
        binInput = binInput.json()

        keyList = []
        scrapedList = []
        scrapedKeys = []
        pageDict = {}



#pull keys from pastebin and put in list
        for i in binInput:
            #print(i)
            keyList.append(i['key'])
        #print(keyList)#test print

#read historical list from file into memory
        #with open(os.path.join('/opt/pybin/python/files/keys/',"scrapedKeys"+".txt"), 'a+') as f:
        try:
            with open('/opt/pybin/python/pybin/files/keys/scrapedKeys.txt') as f:
                scrapedKeys = f.readlines()
            filelogger.debug(scrapedKeys)
            #input
        except IOError:
            with open('/opt/pybin/python/pybin/files/keys/scrapedKeys.txt', 'w+')  as f:
                pass

#remove line break char
        for index, value in enumerate(scrapedKeys):
            scrapedKeys[index] = value.rstrip("\n")
        #print(scrapedKeys)#testprint

#check to see if keyList keys already exist in scrapedKeys, if not skip and write to scrapedList
        for index, value in enumerate(keyList):
            if value in scrapedKeys:
                print(value)
                pass
            else :
                scrapedList.append(keyList[index])

       #print(scrapedList)#print keys to scrape

#Append scrapedKeys File
        with open(os.path.join('/opt/pybin/python/pybin/files/keys/',"scrapedKeys"+".txt"), 'a+') as f:
            for item in scrapedList:
                f.write("%s\n" % item)

#write to scraped list
        with open(os.path.join('/opt/pybin/python/pybin/files/keys/',"scrapedList"+".txt"), 'w+') as f:
            for item in scrapedList:
                 f.write("%s\n" % item)

#get pastes
        for i in scrapedList:
            reqResult = requests.get(rawPasteURL+i)
        #print(reqResult.text)#test print of raw pastes
            pageDict[i] = reqResult.text

        #for k,v in pageDict.items():
            #print(k,v)#test print of dict with pastes

        #print("             ")#spacer
        #change the bellow regex to match what you are looking for.
        refilter = re.compile(r'(?ism)password')
        

        for x,y in pageDict.items():
            result = refilter.findall(y)
    #print(result)
    #print(type(result))
    #print(len(result))
            if len(result) >= 1:
                sep = "*" * 30
                with open(os.path.join('/opt/pybin/python/pybin/files/pastes/',"pasteList"+".txt"), 'a+') as f:
                    f.write("{0} Paste Key: {1} Search Result: {2} URL: {3}\n".format(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),x,result[0], f"https://pastebin.com/{x}"))

        time.sleep(1)

    except Exception as e:
        filelogger.exception("EXCEPTIONSTART", exc_info=True)
        pass
