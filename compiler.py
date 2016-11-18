#!/usr/bin/env python
#coding: utf-8

from scanner import *
from lrparser import Parser
from syntaxer import *
from backend import BackEnd
from translate import Translater
import sys

if __name__ == '__main__':
    try:
        src = sys.argv[1]
    except Exception:
        src = "test.pas"
    else:
        pass
    finally:
        pass
    # import各种类
    sc = Scanner()
    sc.open(src)
    # 定义词法分析器，并打开源文件test.pas
    pa = Parser()
    pa.open("pl0.xml")
    # 定义LR分析器，使用pl0.xml配置
    be = BackEnd("out.txt")
    sy = Syntaxer(be)
    # 定义后端输出的中间代码文件为out.txt
    pa.parser(sc, Token, sy)
    # 编译
    be.close()
    # 关闭中间代码文件
    tr = Translater("out.txt", "res.asm")
    tr.translate()
    tr.close()
    # 将中间代码翻译成汇编
