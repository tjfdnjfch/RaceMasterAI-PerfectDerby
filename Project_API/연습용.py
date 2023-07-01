import datetime
import time
from datetime import timedelta
import requests
from bs4 import BeautifulSoup
import urllib.parse
import xgboost as xgb
import os
import pandas as pd
import sqlite3
import concurrent.futures
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.impute import SimpleImputer
from category_encoders import OrdinalEncoder
from itertools import groupby
import os
import warnings
warnings.filterwarnings('ignore')

DATABASE_PATH = os.path.join(os.getcwd(), 'mymodel/main.db')
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

df=pd.read_csv(os.path.join(os.getcwd(), 'mymodel/경주마 상세정보v2.csv'), index_col=0)

df.to_sql('경주마명', conn, if_exists='replace', index=False)

conn.close()