# -*- coding: utf-8 -*
import readxml
import readcontent
import classifier

readxml.readxml('http://www3.nhk.or.jp/rss/news/cat1.xml', 'social')
readxml.readxml('http://www3.nhk.or.jp/rss/news/cat3.xml', 'science')
readxml.readxml('http://www3.nhk.or.jp/rss/news/cat4.xml', 'politics')
readxml.readxml('http://www3.nhk.or.jp/rss/news/cat5.xml', 'economics')
readxml.readxml('http://www3.nhk.or.jp/rss/news/cat6.xml', 'international')
readxml.readxml('http://www3.nhk.or.jp/rss/news/cat7.xml', 'sports')
readxml.readxml('http://www3.nhk.or.jp/rss/news/cat2.xml', 'culture')
readcontent.readcontent()
print("Finished updating news")
classifier.classifier()
