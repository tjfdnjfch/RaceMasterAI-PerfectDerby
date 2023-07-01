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


def get_lastnday(date_string, n):
  date_format = '%Y%m%d'
  date = datetime.datetime.strptime(date_string, date_format)
  last_month = date - timedelta(days=n)
  last_month_string = last_month.strftime('%Y%m%d')
  return str(last_month_string)  







def get_dateData(name, date, url):
  df = 0
  alert = 0
  ll = 0
  NOR = 250
  skey1 = 'mSuMEgsxd69CVxnw0gh2mQhpq1j9WW1l2%2Beu%2FoY1xZJ56n4yXgThZk4GIrhUh6R1BhWqBKvI5Xddb%2BHrd%2FrXGA%3D%3D'
  skey2 = 'T1PytqZ5KGU3xEUwjx3NB956bZOCpETr1T6gBiY%2BhdTgfZ7sx8iW%2FNnrxh2A5iAyFva4KKkZR1VeXLXr4AXBHw%3D%3D'
  if int(date[-1])%2:
      key = skey1
  else:
      key = skey2
  while True:
    params = {
    'serviceKey' : key,
    'pageNo':'1',
    'numOfRows':str(NOR),
    'meet':'1',
    'rc_date_fr':get_lastnday(date, 365),
    'rc_date_to':get_lastnday(date, 5)
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
    if len(rows)==NOR:
        NOR=round(1.5*NOR)
        continue

        
    if type(df)!=pd.core.frame.DataFrame:
        df = pd.DataFrame(columns=[i.name for i in rows[0].find_all()])
    for k in range(len(rows)):
        tm = {i.name : i.text for i in rows[k].find_all()}
        df = df.append(tm, ignore_index=True)
    break
  if type(df)==pd.core.frame.DataFrame:
    f = open("abc.txt", 'w', encoding="utf8")
    f.write(f"save success : {date}")
    f.close()
    df.to_csv(f"{name}\{date}.csv", encoding="utf-8-sig")
  return df


url = 'https://apis.data.go.kr/B551015/jkpresult/getjkpresult'



name = '경주마기간별50걸명단_365'

try:
  os.mkdir(name)
except:
  pass




file_list = os.listdir('출전 등록말 정보')
temp = [f.rstrip('.csv') for f in list(file_list)]



with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    for date in temp:
        time.sleep(0.3)
        executor.submit(get_dateData(name, date, url))



print("Doing other work here")


