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
        self.ignored = []
        self.data = {}
        self.level_stack = []

    def attribute(self,tag,attrs):
        print('added {0} with attributes:{1}'.format(tag,attrs))
        for k,p in self.attributePath:
            if k == '/'.join(self.level_stack):
                for ak,av in attrs:
                    if ak == p:
                        print('----','/'.join(self.level_stack),ak,av);

    def add(self,tag,attrs):
        for k,v in self.tagAttributs:
            if k != tag:
                continue
            if v:
                for ak,av in attrs:
                    if (ak,av) in v:
                        self.level_stack.append(tag)
                        self.attribute(tag,attrs)
                        return
            else:
                self.level_stack.append(tag)
                self.attribute(tag,attrs)
                return
        self.ignored.append(tag)
        print('{0} ingnored with attributs:{1}'.format(tag,attrs))

    def pop(self,tag):
        if self.ignored and tag == self.ignored[-1]:
            self.ignored.pop()
            return
        if self.level_stack and tag == self.level_stack[-1]:
            self.level_stack.pop()

    def append(self,data):
        pass

