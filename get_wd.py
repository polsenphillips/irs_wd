

import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup 



def generate_urls():
    urls = []
    url = "https://apps.irs.gov/app/picklist/list/writtenDeterminations.html?resultsPerPage=200&sortColumn=number&indexOfFirstRow=0&criteria=&value=&isDescending=true"
    r = requests.get(url)
    iterator = 0
    while r.status_code == 200:
        urls.append(url)
        iterator += 200
        url = "https://apps.irs.gov/app/picklist/list/writtenDeterminations.html?resultsPerPage=200&sortColumn=number&indexOfFirstRow="+ str(iterator) + "&criteria=&value=&isDescending=true"
        r = requests.get(url)    
    print("URLS generated.")    
    return urls

field_names = {}

def parse_soup(urls):##Takes a really long time. Maybe use "lxml" argument?
    table = []
    for url in urls:
        url_req = requests.get(url)
        soup = BeautifulSoup(url_req.content, 'html.parser')
        target_info = soup.findAll(True, {'class':['odd', 'even']})
        for row in target_info:
            values = row.findAll("td")
            url = values[0].find("a").get("href")
            number = values[0].find("a").getText(strip = True)
            uilc = values[1].getText(strip = True)
            subject = values[2].getText(strip = True).replace("&quot;", "'")
            release_date = values[3].getText(strip = True)
            table.append([url, number, uilc, subject, release_date])  
    print("Table populated.")    
    return table


df = pd.DataFrame(data = table)

def add_header():
    df.columns = ["url", "number", "uilc", "subject", "release_date"]
    return df  

def main():
    parse_soup(generate_urls())
    
    add_header()
    df.to_csv("written_determinations_{0}.csv".format(str(datetime.date.today())))


if __name__ == "__main__":
    main()








