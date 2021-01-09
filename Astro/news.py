#!/usr/bin/python3
# -*- coding: ascii -*-

import cgi
import cgitb; cgitb.enable()

import feedparser

print("Content-type: text/html;charset=utf-8")
print("""
<html>
<head>
<title>Almanac</title>
</head>
<body>""")


def getNews(nm, fd, n):
    bag = []
    bag.append("<font color='yellow'>" + nm + "</font>")
    fp = feedparser.parse(fd)
    for e in fp.entries[0:n]:
        #r = e.published.split(' ')[4] + ' ' + e.title
        r = e.title
        asciidata=r.encode("ascii","ignore").decode()
        bag.append(asciidata)
    tbl_template = ('<tr>%s</tr>' % ("<td class='n'>%s</td>" ) * (len(bag)))
    return (tbl_template % tuple(bag))

print("<table width=100% height=100%>")
print("<td style='vertical-align:text-top;'><table>")
print(getNews('NYT', 'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml', 8))
print("</table></td>")
print("<td style='vertical-align:text-top;'><table>")
print(getNews('Post', 'http://nypost.com/feed/', 5))
print("</table></td>")
print("<td style='vertical-align:text-top;'><table>")
print(getNews('Drudge', 'http://feeds.feedburner.com/DrudgeReportFeed', 5))
print("</table></td>")
print("</table>")

print("</body>")
print("</html>")
