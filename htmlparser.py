#!/usr/bin/python
# -*- coding:utf-8 -*-

from html.parser import HTMLParser
from MatchLinkParser import MatchLinkParser
from SquadParser import SquadParser

class htmlparser(HTMLParser):
    linkParser = MatchLinkParser()
    squadParser = SquadParser()
    def __init(self):
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        self.linkParser.add(tag,attrs)
        self.squadParser.add(tag,attrs)

    def handle_endtag(self, tag):
        self.linkParser.pop(tag)
        self.squadParser.pop(tag)

    def handle_data(self, data):
        self.linkParser.append(data)
        self.squadParser.append(data)

parser = htmlparser()
with open('f.txt',encoding='utf-8') as fi:
    parser.feed(fi.read())

print(parser.squadParser.getdata())
parser.close()
