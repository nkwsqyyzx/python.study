#!/usr/bin/python
# -*- coding:utf-8 -*-
from html.parser import HTMLParser

class PLAYERTYPE:
    # 是否是首发球员 -1 其他 0 首发球员，1 替补上场，2 未上场队员
    NONE = -1
    # 其他
    FIRST = 0
    # 首发
    SUBSTITUTEIN = 1
    # 替补上场
    NOSUBSTITUE = 2
    # 未替补上场

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
        self.data = [[],[],[],[],[],[]]
        self.playerType = PLAYERTYPE.NONE
        self.shirtnumber = 0
        self.link = ''
        self.ignored_tag = []
        self.tag_stack = []
        self.substitutionIn = ''
        self.substitutionOut = ''
        self.hostSquad = -1
        self.hostSubstitute = -1

    def tagPath(self):
        return '/'.join([i for i,j,k in self.tag_stack])

    def attribute(self,tag,attrs):
        tagPath = self.tagPath()
        if not attrs:
            return
        for k,p in self.attributePath:
            if k == tagPath:
                self.link = self.getKV(attrs,p)

    def add(self,tag,attrs):
        if tag == 'table':
            if self.tag_stack:
                raise RuntimeError('too much tables {0}'.format(attrs))
            if self.hasKV(attrs,'class','playerstats lineups table'):
                # 首发球员表
                self.tag_stack.append((tag,'',''))
                self.playerType = PLAYERTYPE.FIRST
                self.ignored_tag.clear()
                self.hostSquad += 1
                return
            elif self.hasKV(attrs,'class','playerstats lineups substitutions table'):
                # 替补球员表
                self.tag_stack.append((tag,'',''))
                self.ignored_tag.clear()
                self.hostSubstitute += 1
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
            self.ignored_tag.pop()
            return
        if self.tag_stack and tag == self.tag_stack[-1][0]:
            self.tag_stack.pop()
            if tag == 'table':
                self.playerType = PLAYERTYPE.NONE
            
    #self.dataPath = ['table/tbody/tr/td','table/tbody/tr/td/a','table/tbody/tr/td/p','table/tbody/tr/td/p/a']
    def append(self,data):
        sz = data.strip()
        if not sz :
            return
        path = self.tagPath()
        if path == 'table/tbody/tr/td':
            # 首发、替补的号码
            self.shirtnumber = int(sz)
        elif path == 'table/tbody/tr/td/a':
            # 首发的名字
            if self.playerType == PLAYERTYPE.FIRST:
                self.data[self.hostSquad].append((self.shirtnumber, sz, self.link))
                self.shirtnumber = 0
                self.link = ''
        elif path == 'table/tbody/tr/td/p':
            if sz == 'for':
                # 前面是替补上场的队员,后面是替补下场的队员.
                self.playerType = PLAYERTYPE.SUBSTITUTEIN
            elif self.playerType == PLAYERTYPE.SUBSTITUTEIN:
                # 替补上场的时间
                # (替补球员,时间,首发球员)
                self.data[self.hostSubstitute+2].append((self.substitutionIn,sz,self.substitutionOut))
                self.playerType = PLAYERTYPE.NONE
                
        elif path == 'table/tbody/tr/td/p/a':
            # 替补上场的球员
            if self.playerType == PLAYERTYPE.SUBSTITUTEIN:
                self.substitutionOut = sz
            elif not self.playerType == PLAYERTYPE.SUBSTITUTEIN:
                self.substitutionIn = sz
                # 这里是所有替补队员
                self.data[self.hostSubstitute+4].append(sz)

    def getdata(self):
        "返回所有数据,[0]->主队首发 [1]->客队首发 [2]->主队换人信息 [3]->客队换人信息 [4]->主队所有替补 [5]->客队所有替补"
        return self.data

# test code
if __name__ == '__main__':   
    from htmlparser import htmlparser     
    parser = htmlparser()
    with open('f.txt',encoding='utf-8') as fi:
        parser.feed(fi.read())
    parser.close()
