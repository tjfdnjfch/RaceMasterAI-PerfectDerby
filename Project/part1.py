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


import functions




DATABASE_PATH = os.path.join(os.getcwd(), 'main.db')
conn = sqlite3.connect(DATABASE_PATH)


URL = 'https://race.kra.co.kr/dbdata/textData.do?Act=12&Sub=1&meet=1'

driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url=URL)



link = '경마성적표'
posting = driver.find_element(By.LINK_TEXT, link)
posting.click()





soup = BeautifulSoup(driver.page_source, 'html.parser')
lastno = int(soup.find('a',{'class':'next2'})['href'].lstrip("?pageIndex="))


prefix = "https://race.kra.co.kr//dbdata/fileDownLoad.do?fn="


for pageno in range(1, lastno+1):
    if (pageno%10 == 1) and (pageno != 1):
        posting = driver.find_element(By.CLASS_NAME, 'next')
    else:
        posting = driver.find_element(By.LINK_TEXT, str(pageno))
        
    posting.click()


    soup = BeautifulSoup(driver.page_source, 'html.parser')


    temp = [prefix + t['onclick'].split("'")[1] for t in soup.find('tbody').find_all('a')]


    for url in temp:
        functions.appendtable(link, url, conn)



breakpoint()
