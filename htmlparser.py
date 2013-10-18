#!/usr/bin/python
# -*- coding:utf-8 -*-

from html.parser import HTMLParser

class MatchLinkParser:
    def __init__(self):
        self.tagAttributs = (
                ('div',[('class','form clearfix'),('class','clearfix'),('class','container left'),('class','container right')]),
                ('h3',[('class','thick')]),
                ('a',[]))
        self.attributePath = (('div/div/h3/a','href'),('div/div/div/a','href'),('div/div/div/a','title'))
        self.data = {}
        self.level_stack = []

    def attribute(self,attrs):
        for k,p in self.attributePath:
            if k == '/'.join(self.level_stack):
                for ak,av in attrs:
                    if ak == p:
                        print('/'.join(self.level_stack),ak,av);

    def add(self,tag,attrs):
        for k,v in self.tagAttributs:
            if k != tag:
                continue
            if v:
                for ak,av in attrs:
                    if (ak,av) in v:
                        self.level_stack.append(tag)
                        self.attribute(attrs)
                        return
            else:
                self.level_stack.append(tag)
                self.attribute(attrs)
                return

    def pop(self,tag):
        if self.level_stack and tag == self.level_stack[-1]:
            self.level_stack.pop()

    def append(self,data):
        pass

class PageParser(HTMLParser):
    def __init(self):
        self.linkParser = MatchLinkParser()
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        self.linkParser.add(tag,attrs)

    def handle_endtag(self, tag):
        self.linkParser.pop(tag)

    def handle_data(self, data):
        self.linkParser.append(data)

class SoccerWayHtmlParser(HTMLParser):
    def __init__(self):
        self.tagAttributs = ( 
            ('table',[('class','playerstats lineups table')],[]),
            ('tbody',[],[]),
            ('tr',[('class','odd'),('class','even')],[]),
            ('td',[('class','shirtnumber'),('class',"player large-link")]),
            ('a',[],['href']))
        self.valuepaths = ['table/tbody/tr/td','table/tbody/tr/td/a']
        HTMLParser.__init__(self)

    def reset(self):
        HTMLParser.reset(self)
        self.level_stack = []
        
    def add(self,tag):
        self.level_stack.append(tag)
        
    def pop(self,tag):
        if self.level_stack and tag == self.level_stack[-1]:
            self.level_stack.pop()

    def handle_starttag(self, tag, attrs):
        for k,v in self.tagAttributs:
            if k == tag:
                if v:
                    for ak,av in attrs:
                        if (ak,av) in v:
                            self.add(tag)
                            return
                else:
                    self.add(tag)
                    return

    def handle_endtag(self, tag):
        self.pop(tag)

    def handle_data(self, data):
        if '/'.join(self.level_stack) in self.valuepaths and data.strip():
            print('/'.join(self.level_stack), data.strip())

parser = PageParser()
with open('href.html',encoding='utf-8') as fi:
    parser.feed(fi.read())
parser.close()
