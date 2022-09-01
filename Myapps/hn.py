from bs4 import BeautifulSoup
from datetime import datetime
import requests

def req_data():
    res = requests.get("https://news.ycombinator.com/")
    soup = BeautifulSoup(res.text, "html.parser")
    titles = soup.select(".titlelink")
    subs = soup.select(".subtext")
    return titles, subs

def filter_rec(t, subtext):
    new_records = []
    for ind, title in enumerate(t):
        title_link = title.get("href", None) # , default
        vote = subtext[ind].select(".score")
        if len(vote):
            scoring = int(vote[0].text.split()[0])
            if scoring > 100:
                new_records.append((title.text, title_link, subtext[ind], scoring))
    return Sort(new_records)

def Sort(data):
    if type(data)!=str:
        return sorted(data, key=lambda k:k[3], reverse=True)

def publish():
    title, subtexts = req_data()
    today = str(datetime.now().strftime("News for %d/%m/%y, %a at %H:%M"))
    titles, links, votes, = [], [], []
    for t, a, subt, v in filter_rec(title, subtexts):
        titles.append(t)
        links.append(a)
        votes.append(v)
    return (titles, links, votes, today)
if __name__ == '__main__':
    t, a, v, to = publish()
    print(t[1])
    print(a[1])
    print(v[1])
    print(to)