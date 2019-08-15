from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)


@app.route("/")
def index():
    table = create_df(
        "https://www.tiket.com/kereta-api/cari?d=GMR&dt=STATION&a=BD&at=STATION&date=2019-08-24&ret_date=2019-08-25&adult=1&infant=0"
    ).to_html(classes=["table table-bordered table-striped table-dark table-condensed"])
    return render_template("index.html", table=table)


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


@app.route("/html/departure")
def departure_table():
    df = create_df(
        "https://www.tiket.com/kereta-api/cari?d=GMR&dt=STATION&a=BD&at=STATION&date=2019-08-24&ret_date=2019-08-25&adult=1&infant=0"
    )
    return df.to_html()


@app.route("/charts/departure")
def departure_charts():
    import altair as alt

    df = create_df(
        "https://www.tiket.com/kereta-api/cari?d=GMR&dt=STATION&a=BD&at=STATION&date=2019-08-24&ret_date=2019-08-25&adult=1&infant=0"
    )
    chart = (
        alt.Chart(df)
        .encode(
            x="depart_time", y="price", tooltip=["depart_time", "arrive_time", "price"]
        )
        .mark_line(interpolate="basis", color="#19615b")
    )
    return chart.to_json()


if __name__ == "__main__":
    app.run()
