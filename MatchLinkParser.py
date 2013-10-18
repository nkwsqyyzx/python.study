#!/usr/bin/python
# -*- coding:utf-8 -*-
from html.parser import HTMLParser

class MatchLinkParser:
    def __init__(self):
        self.divlevel = [
                {('class','clearfix')},
                {('class','container right'),('class','container left')},
                {('class','form clearfix')}]

        self.tagAttributs = (('h3',[('class','thick')]),('a',[]))
        self.attributePath = (('div/div/div/a','href'),('div/div/div/a','title'))
        self.data = []
        self.ignored_tag = []
        self.tag_stack = []
        self.title = ''
        self.link = ''

    def tagPath(self):
        return '/'.join([i for i,j,k in self.tag_stack])

    def attribute(self,tag,attrs):
        tagPath = self.tagPath()
        for k,p in self.attributePath:
            if k == tagPath:
                for ak,av in attrs:
                    if ak == p :
                        if ak == 'title':
                            self.title = av
                        elif ak == 'href':
                            self.link = av
        if self.link and self.title:
            self.data.append((self.title,self.link))
            self.link = ''
            self.title = ''


    def add(self,tag,attrs):
        div_stack = [i for i,(j,k,l) in enumerate(self.tag_stack) if j == 'div']
        setIndex = (div_stack[-1] + 1) if div_stack else 0;
        if tag == 'div':
            if setIndex < len(self.divlevel):
                setDivProperty = self.divlevel[setIndex] & set(attrs)
                if setDivProperty:
                    (i,j) = setDivProperty.pop();
                    self.tag_stack.append((tag,i,j))
                    self.ignored_tag.clear()
                    return
            else:
                print('too much divs.',attrs)
        elif setIndex > 0:
            for k,v in self.tagAttributs:
                if k != tag:
                    continue
                if v:
                    for ak,av in attrs:
                        if (ak,av) in v:
                            self.tag_stack.append((tag,ak,av))
                            self.ignored_tag.clear()
                            self.attribute(tag,attrs)
                            return
                else:
                    self.tag_stack.append((tag,'',''))
                    self.ignored_tag.clear()
                    self.attribute(tag,attrs)
                    return
        self.ignored_tag.append(tag)

    def pop(self,tag):
        if self.ignored_tag and tag == self.ignored_tag[-1]:
            a = self.ignored_tag.pop()
            return
        if self.tag_stack and tag == self.tag_stack[-1][0]:
            a = self.tag_stack.pop()

    def append(self,data):
        pass


    def getdata(self):
        return self.data
