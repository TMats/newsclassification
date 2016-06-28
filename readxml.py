# -*- coding: utf-8 -*
def readxml(URL, cat):
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    from datetime import datetime
    import mysql.connector
    import config

    # mysql
    con = mysql.connector.connect(
        host=config.host,
        db=config.db,
        user=config.user,
        passwd=config.passwd,
        buffered=True)
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS newsclassification.news(id int(11), pubdate datetime, url varchar(255), category text, content mediumtext)""")

    # scraping
    f = urlopen(URL)
    soup_xml = BeautifulSoup(f, "html.parser")
    dataset = []
    for item in soup_xml.find_all('item'):
        link = item.find('link').text
        time = datetime.strptime(item.find('pubdate').string, '%a, %d %b %Y %H:%M:%S %z')
        dataset = dataset+[(time, link, cat)]

    add_link = ("INSERT IGNORE INTO news " "(pubdate, url, category) " "VALUES (%s, %s, %s)")
    for data in dataset:
        cur.execute(add_link, data)

    con.commit()
    cur.close()
    con.close()

if __name__ == "__main__":
    readxml('http://www3.nhk.or.jp/rss/news/cat1.xml', 'social')
    readxml('http://www3.nhk.or.jp/rss/news/cat3.xml', 'science')
