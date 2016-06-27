# -*- coding: utf-8 -*
def readcontent():
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

    cur.execute("""SELECT id, url FROM news WHERE content IS NULL""")
    record = cur.fetchone()
    while record != None:
        sqlid = record[0]
        link = record[1].encode('utf-8').decode('ASCII')
        print("Updating News: "+link)
        g = urlopen(link)
        soup_article = BeautifulSoup(g, "html.parser")
        textbody = soup_article.find("div", attrs={"id": "news_textbody"}).text
        textmore = soup_article.find("div", attrs={"id": "news_textmore"}).text
        text = textbody + textmore
        cur2 = con.cursor()
        cur2.execute("""UPDATE news SET content = %s where id = %s""", (text, sqlid))
        cur2.close()
        record = cur.fetchone()

    con.commit()
    cur.close()
    con.close()

if __name__ == "__main__":
    readcontent()
