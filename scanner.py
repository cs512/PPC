#! /usr/bin/python
#coding: utf-8

import re

class Token():
    u"""Token类型保存了每个Token所在行列以及类型与原文"""
    def __init__(self, row = 1, col = 1, content = "", token_type = ""):
        self.row = row
        self.col = col
        self.content = content
        self.token_type = token_type

    def __str__(self):
        return str((self.row, self.col, self.content, self.token_type))

class Scanner():
    u"""scanner提供了一个通用的语法扫描器，通过迭代的方式返回token类型"""
    re_str = r'PROCEDURE|BEGIN|END|CONST|VAR|WHILE|DO|IF|THEN|ODD|CALL|INT|OUT|IN|ELSE|READ|WRITE|[a-zA-Z_]\w*|\d+|\+|-|\*|/|:=|=|<>|<=|>=|<|>|\(|\)|\;|\,|\s|\.'
    scan = re.compile(re_str)
    keywords = ('PROCEDURE', 'BEGIN', 'END', 'CONST', 'VAR', 'WHILE', 'DO', 'IF', 'THEN', 'ODD', 'CALL', 'INT', 'OUT', 'IN', 'ELSE', 'READ', 'WRITE')
    operator = ('+', '-', '*', '/', ':=', '=', '<>', '<', '>', '>=', '<=')
    delimiter = ('(', ')', ';', ',', '.')
    number = (tuple)([str(i) for i in range(10)])
    lower_letter = (tuple)([chr(ord('a') + i) for i in range(26)])
    upper_letter = (tuple)([chr(ord('A') + i) for i in range(26)])
    space = (' ', '\t', )

    def __init__(self):
        self.fin = None
        self.tokens = []
        self.row = 1
        self.col = 1

    def check_type(self, c_str):
        # print (c_str)
        if c_str in Scanner.keywords:
            return "KEYWORD"
        if c_str in Scanner.operator:
            return "OPERATOR"
        if c_str in Scanner.delimiter:
            return "DELIMTER"
        if c_str[0] in Scanner.number:
            return "CONST"
        if c_str[0] in Scanner.upper_letter:
            return "IDENT"
        if c_str[0] in Scanner.lower_letter:
            return "IDENT"
        if c_str[0] in Scanner.space:
            return "SPACE"
        if c_str[0] == '\n':
            return "RETURN"
        return 'UNKNOW'

    def open(self, name):
        u"""打开一个源文件"""
        self.fin = file(name, "r")
        temp_str = self.fin.read()
        self.tokens = Scanner.scan.findall(temp_str)
        self.tokens = iter(self.tokens)
        return self.fin

    def __iter__(self):
        return self

    def next(self):
        u"""迭代器next函数，用于每次返回token"""
        if self.fin == None:
            raise StopIteration
        cont =  self.tokens.next()
        token_type = self.check_type(cont)
        while(token_type in ("SPACE", "UNKNOW", "RETURN")):
            if(token_type == "RETURN"):
                self.row += 1
                self.col = 1
            else:
                self.col += len(cont)
            cont =  self.tokens.next()
            token_type = self.check_type(cont)
        if token_type in ("KEYWORD", "OPERATOR", "DELIMTER"):
            token_type = '"{0}"'.format(cont)
        r_token = Token(row = self.row, col = self.col, content = cont, token_type = token_type)
        self.col += len(cont)
        return r_token

    
