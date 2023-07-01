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

def get_dateData(name, date, url):
  df = 0
  alert = 0
  ll = 0
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
    'numOfRows':'250',
    'meet':'1',
    'pg_date':date,
    '_type':'xml'
    }
    headers = {
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    }
    query_string = urllib.parse.urlencode(params, safe="%")

    url_mod = f"{url}?{query_string}"
    time.sleep(0.7)
    response = requests.get(url_mod, headers=headers, verify = False)
    xmlobj = BeautifulSoup(response.text.encode('utf-8'), 'lxml-xml')
    rows = xmlobj.findAll('item')
    if len(rows)==0 and 'NORMAL SERVICE' in str(response.text.encode('utf-8')):
        break
    if 'NORMAL SERVICE' not in str(response.text.encode('utf-8')):
        print(str(response.text.encode('utf-8')))
        print(f"{rows}:{date}")
        raise

        
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


url = 'https://apis.data.go.kr/B551015/API23_1/entryRaceHorse_1'



name = '출전 등록말 정보'


start_date = "2018-07-17"
end_date = "2023-01-01"

dates = pd.date_range(start_date, pd.to_datetime(end_date) + pd.Timedelta(days=10))
date_strings = [d.strftime("%Y%m%d") for d in dates]



# os.mkdir(name)




with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    for date in date_strings:
        time.sleep(0.3)
        executor.submit(get_dateData(name, date, url))



print("Doing other work here")






