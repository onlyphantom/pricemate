import requests
from bs4 import BeautifulSoup
import pandas as pd


def collecthtml(url):
    url = requests.get(url)
    htmlcontent = url.content.decode("utf-8").replace("\n", "")
    soup = BeautifulSoup(htmlcontent, "html.parser")
    return soup


def depart(url):
    soup = collecthtml(url)
    depart_table = soup.find(id="tbody_depart")
    all_departures = dict()
    i = 0
    for tr in depart_table.findAll("tr"):
        tds = tr.findAll("td")
        title = tds[1].find("div").text.replace("\t", "")
        dt = tds[2].find("div").text
        at = tds[3].find("div").text
        price = tds[4].find("div").text
        dic = dict(title=title, depart_time=dt, arrive_time=at, price=price)
        # print(dic)
        all_departures[i] = dic
        i += 1
    return all_departures


def create_df(url, sort=False):
    dicr = depart(url)
    df = pd.DataFrame(dicr).T
    df["price"] = df["price"].str.replace("[^0-9]", "")

    if sort:
        df["depart_time"] = pd.to_datetime(df["depart_time"])
        df.sort_values("depart_time")
    return df


# Testing / Development:
# url = "https://www.tiket.com/kereta-api/cari?d=GMR&dt=STATION&a=BD&at=STATION&date=2019-08-24&ret_date=2019-08-25&adult=1&infant=0"
# df = create_df(url)

