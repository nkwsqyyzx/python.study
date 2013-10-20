#!/usr/bin/python
# -*- coding:utf-8 -*-
from html.parser import HTMLParser

class SquadParser:

    def hasKV(self,attrs,ak,av):
        kvs = [(i,j) for (i,j) in attrs]
        if kvs:
            return (ak,av) in kvs
        else:
            return False
        
    def getKV(self,attrs,k):
        kvs = [(i,j) for (i,j) in attrs if k == i]
        if len(kvs) == 1:
            return kvs[0][1]
        return None

    def __init__(self):
        self.tablelevel = [{('class','playerstats lineups table')}]
        self.tagAttributs = (
                ('tbody',[]),
                ('tr',[('class','odd'),('class','even')]),
                ('td',[('class','shirtnumber'),('class','player large-link')]),
                ('p',[('class','substitute substitute-in'),('class','substitute substitute-out')]),
                ('a',[]))
        self.attributePath = [('table/tbody/tr/td/a','href')]
        self.dataPath = ['table/tbody/tr/td','table/tbody/tr/td/a','table/tbody/tr/td','table/tbody/tr/td/p','table/tbody/tr/td/p/a']
        self.data = []
        self.shirtnumber = 0
        self.name = ''
        self.isvalid = 0
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
                self.link = self.getKV(attrs,p)

    def add(self,tag,attrs):
        if tag == 'table':
            if self.tag_stack:
                raise RuntimeError('too much tables {0}'.format(attrs))
            if self.hasKV(attrs,'class','playerstats lineups table'):
                self.tag_stack.append((tag,'',''))
                self.ignored_tag.clear()
                return
            elif self.hasKV(attrs,'class','playerstats lineups substitutions table'):
                self.tag_stack.append((tag,'',''))
                return
            else:
                # invalid table tag
                pass
        elif self.tag_stack:
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
        sz = data.strip();
        path = self.tagPath()
        if sz:
            if path == 'table/tbody/tr/td':
                self.shirtnumber = int(sz)
            elif path == 'table/tbody/tr/td/a':
                self.name = sz
            else:
                # wrong path
                pass
            
        if self.name:
            self.data.append((self.shirtnumber,self.link,self.name))
            self.name = ''
            self.link = ''
            self.shirtnumber = 0
            
    def getdata(self):
        return self.data
