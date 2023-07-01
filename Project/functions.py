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

def appendtable(link, url, conn):
    if link == '경마성적표':
        appendtable_경마성적표(link, url, conn)
    pass


def appendtable_경마성적표(link, url, conn):
    source = requests.get(url).text
    i=0
    for df0 in source.split('제목')[1:]:
        try:
            ground_date = 0
            ground_no= 0
            ground_dist =0
            temp = re.split(r"-{5,}", df0)
            tableA = temp[0]
            ground_date = re.search(r'\d\d\년\d\d\월\d\d일', tableA).group(0)
            ground_no= re.search(r'제\s*\d+경주', tableA).group(0)
            ground_no= int(re.search(r'\d{1,2}', ground_no).group(0))
            ground_dist = re.search(r'\d{2,5}M', tableA).group(0)
            ground_dist = int(re.search(r'\d{2,5}', ground_dist).group(0))
            tableB = temp[1]+temp[2]
            regex = re.compile(r"\(((?!주).+?)\)")
            tableB = regex.sub(" "*4, tableB)
            pattern = re.compile(r"\s*마(\s+?)명\s*")
            tableB = pattern.sub(lambda m: f"  마명{' '*(4*len(m.group(1))-1)}", tableB)
            dfB = pd.read_csv(io.StringIO(tableB), sep='\s{2,}', header=0)
            dfB = dfB.assign(경주일자=ground_date, 경주번호=ground_no, 경주거리=ground_dist)

            dfB.to_sql(link, conn, if_exists='append')
            i+=1
        except:
            print(url)
            print(i)
            breakpoint()

    pass

