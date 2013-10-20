#!/usr/bin/python
# -*- coding:utf-8 -*-
from html.parser import HTMLParser

class PLAYERTYPE:
    # 是否是首发球员 -1 其他 0 首发球员，1 替补上场，2 未上场队员
    NONE = -1
    # 首发
    FIRST = 0
    # 替补上场
    SUBSTITUTE = 1
    # 未替补上场
    NOSUBSTITUE = 2

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
        self.data = []
        self.playerType = PLAYERTYPE.NONE
        self.shirtnumber = 0
        self.name = ''
        self.link = ''
        self.ignored_tag = []
        self.tag_stack = []

    def tagPath(self):
        return '/'.join([i for i,j,k in self.tag_stack])

    def attribute(self,tag,attrs):
        tagPath = self.tagPath()
        if not attrs:
            return
        for k,p in self.attributePath:
            if k == tagPath:
                self.link = self.getKV(attrs, p)

    def add(self,tag,attrs):
        if tag == 'table':
            if self.tag_stack:
                raise RuntimeError('too much tables {0}'.format(attrs))
            if self.hasKV(attrs,'class','playerstats lineups table'):
                # 首发球员表
                self.tag_stack.append((tag,'',''))
                self.playerType = PLAYERTYPE.FIRST
                self.ignored_tag.clear()
                return
            elif self.hasKV(attrs,'class','playerstats lineups substitutions table'):
                # 替补球员表
                self.tag_stack.append((tag,'',''))
                self.ignored_tag.clear()
                return
            else:
                pass
        elif self.tag_stack:
            for k,v in self.tagAttributs:
                if k != tag:
                    continue
                if k == 'p':
                    self.playerType = PLAYERTYPE.SUBSTITUTE
                
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
            self.ignored_tag.pop()
            return
        if self.tag_stack and tag == self.tag_stack[-1][0]:
            self.tag_stack.pop()
            if tag == 'table':
                self.playerType = PLAYERTYPE.NONE
            
    #self.dataPath = ['table/tbody/tr/td','table/tbody/tr/td/a','table/tbody/tr/td/p','table/tbody/tr/td/p/a']
    def append(self,data):
        d = data.strip()
        if not d :
            return
        tagPath = self.tagPath()
        if tagPath == 'table/tbody/tr/td':
            # 首发、替补的号码
            self.shirtnumber = int(d)
        elif tagPath == 'table/tbody/tr/td/a':
            # 首发的名字
            self.name = d
        elif tagPath == 'table/tbody/tr/td/p':
            # 替补
            # print(tagPath,d)
            pass
        elif tagPath == 'table/tbody/tr/td/p/a':
            pass
            # print(tagPath,d)

        if self.playerType == PLAYERTYPE.SUBSTITUTE:
            print('substitutions',d)
        
        if self.name:
            if self.playerType == PLAYERTYPE.FIRST:
                self.data.append((self.shirtnumber, self.name, self.link))
                self.shirtnumber = 0
                self.name = ''
                self.link = ''

    def getdata(self):
        return self.data
