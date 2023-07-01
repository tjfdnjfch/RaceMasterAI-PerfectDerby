import os

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


name_list = ['경주성적정보', '기수기간별성적비교','마주기간별성적비교','조교사기간별전적비교','출전 등록말 정보', '출전표 상세정보']

for name in name_list:
    files= os.listdir(f"./{name}")
    files.sort()
    df_all = pd.DataFrame()
    for file in files:
        df=pd.read_csv(f"./{name}/{file}", encoding='utf-8')
        df = df.assign(MatchingPeriod=int(file.rstrip('.csv')))
        df_all = pd.concat([df_all, df], ignore_index=True)
        df_all = df_all.drop(labels="Unnamed: 0", axis=1)
    if ('기간별' in name) and ('50걸' not in name):
        df_all = df_all.rename(columns=lambda x: x + name[:2])
    df_all.to_csv(f'./total/{name}.csv', index=False, encoding="utf-8-sig")