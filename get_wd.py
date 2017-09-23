import pandas as pd
import pprint
import seaborn as sns
import matplotlib.pyplot as plt

import requests
import grequests
from bs4 import BeautifulSoup

url_list = []
last_current_url = "https://apps.irs.gov/app/picklist/list/writtenDeterminations.html?indexOfFirstRow=61400&sortColumn=number&value=&criteria=&resultsPerPage=200&isDescending=true"
url_1 = "https://apps.irs.gov/app/picklist/list/writtenDeterminations.html?resultsPerPage=200&sortColumn=number&indexOfFirstRow=0&criteria=&value=&isDescending=true"
url_1_req = requests.get(url_1)

soup = BeautifulSoup(url_1_req.content, 'html.parser')
target_info = soup.findAll(True, {'class':['odd', 'even']})

table = []

for row in target_info:
    values = row.findAll("td")
    url = values[0].find("a").get("href")
    number = values[0].find("a").getText(strip = True)
    uilc = values[1].getText(strip = True)
    subject = values[2].getText(strip = True).replace("&quot;", "'")
    release_date = values[3].getText(strip = True)
    table.append([url,number, uilc, subject, release_date])
    

