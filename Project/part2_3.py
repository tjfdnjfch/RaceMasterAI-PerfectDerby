import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

import requests
from bs4 import BeautifulSoup

import re

import io
import pandas as pd

import os
import sqlite3


import urllib.parse

import warnings

warnings.filterwarnings("ignore")

import concurrent.futures


import time

import datetime
from datetime import timedelta

import random





def get_Data(name, url):
  df = 0
  alert = 0
  ll = 0
  NOR = 200
  pgno = 0
  while True:
    skey1 = 'mSuMEgsxd69CVxnw0gh2mQhpq1j9WW1l2%2Beu%2FoY1xZJ56n4yXgThZk4GIrhUh6R1BhWqBKvI5Xddb%2BHrd%2FrXGA%3D%3D'
    skey2 = 'T1PytqZ5KGU3xEUwjx3NB956bZOCpETr1T6gBiY%2BhdTgfZ7sx8iW%2FNnrxh2A5iAyFva4KKkZR1VeXLXr4AXBHw%3D%3D'
    if random.random() >= 0.5:
        key = skey1
    else:
        key = skey2
    pgno += 1
    params = {
    'serviceKey' : key,
    'pageNo':str(pgno),
    'numOfRows':'2000',
    'meet':'1'
    }
    headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    query_string = urllib.parse.urlencode(params, safe="%")

    url_mod = f"{url}?{query_string}"
    f = open("abd.txt", 'w', encoding="utf8")
    f.write(url_mod)
    f.close()
    time.sleep(0.7)
    response = requests.get(url_mod, headers=headers, verify = False)
    xmlobj = BeautifulSoup(response.text.encode('utf-8'), 'lxml-xml')
    rows = xmlobj.findAll('item')
    if len(rows)==0 and 'NORMAL SERVICE' in str(response.text.encode('utf-8')):
        break
    if 'NORMAL SERVICE' not in str(response.text.encode('utf-8')):
        f = open("abc.txt", 'w', encoding="utf8")
        f.write(str(response.text.encode('utf-8')))
        f.write(f"{rows}:{date}")
        f.close()
        raise

        
    if type(df)!=pd.core.frame.DataFrame:
        df = pd.DataFrame(columns=[i.name for i in rows[0].find_all()])
    for k in range(len(rows)):
        tm = {i.name : i.text for i in rows[k].find_all()}
        df = df.append(tm, ignore_index=True)
    if len(rows)==2000:
        continue
    break
  if type(df)==pd.core.frame.DataFrame:
    f = open("abc.txt", 'w', encoding="utf8")
    f.write(f"save success : {name}")
    f.close()
    df.to_csv(f"{name}/{name}.csv", encoding="utf-8-sig")
  return df


url = 'https://apis.data.go.kr/B551015/API8_1/raceHorseInfo_1'



name = '경주마 상세정보'

try:
  os.mkdir(name)
except:
  pass




file_list = os.listdir('출전 등록말 정보')
temp = [f.rstrip('.csv') for f in list(file_list)]


get_Data(name, url)



print("Doing other work here")


