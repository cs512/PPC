#! /usr/bin/python
#coding: utf-8

import xml.etree.cElementTree as element_tree

class XmlDecodeError(Exception):
    """docstring for XmlDecodeError Exception"""
    def __init__(self, string):
        Exception.__init__(self)
        return

class ParseringError(Exception):
    """docstring for XmlDecodeError Exception"""
    def __init__(self, token, state):
        Exception.__init__(self)
        self.token = token
        self.state = state
        return

class Transition(object):
    """docstring for Transition"""
    def __init__(self, type = "", symbol = "", state = -1, rule = ""):
        self.type = type
        self.symbol = symbol
        self.state = state
        self.rule = rule

class Rule(object):
    """docstring for Rule"""
    def __init__(self):
        self.lhs = ""
        self.rhs = []
        self.number = -1

    def __str__(self):
        return "{0}".format((self.number, self.lhs, self.rhs))

class Parser(object):
    """docstring for parser"""
    def __init__(self):
        pass

    def open(self, name):
        self.symbol_stack = []
        self.state_stack = []
        self.syntax_stack = []

        self.tree = element_tree.ElementTree(file = name)
        self.root = self.tree.getroot()
        print(self.root.tag, self.root.attrib)
        try:
            self.grammar = self.root.find('grammar')
        except Exception:
            raise XmlDecodeError, "On grammar. Please using bison compatible xml file."

        self.rules = []
        try:
            trules = self.grammar.find('rules')
            count = 0
            for node in trules:
                trule = Rule()
                trule.lhs = node.find('lhs').text
                trule.number = int(node.attrib['number'])
                if count != trule.number:
                    raise XmlDecodeError, "On rules/lhs|rhs|number. Please using bison compatible xml file."
                count += 1
                for rhss in node.find('rhs'):
                    if rhss.text != None:
                        trule.rhs.append(rhss.text)
                self.rules.append(trule)
        except Exception:
            raise XmlDecodeError, "On rules/lhs|rhs|number. Please using bison compatible xml file."
        
        self.terminals = []
        try:
            tterminals = self.grammar.find('terminals')
            for node in tterminals:
                self.terminals.append(node.attrib['name'])
        except Exception:
            raise XmlDecodeError, "On terminals/name. Please using bison compatible xml file."
        
        self.nonterminals = []
        try:
            tnonterminals = self.grammar.find('nonterminals')
            for node in tnonterminals:
                self.nonterminals.append(node.attrib['name'])
        except Exception:
            raise XmlDecodeError, "On nonterminals/name. Please using bison compatible xml file."
        
        self.automaton = []

        tautomaton = self.root.find('automaton')
        count = 0
        for node in tautomaton:
            if node.tag != 'state' or count != int(node.attrib['number']):
                raise XmlDecodeError, "On automaton. Please using bison compatible xml file."
            count += 1
            actions = node.find('actions')
            t_state = {}
            try:
                transitions = actions.find('transitions')
                for tran in transitions:
                    t_transition = Transition(  type    = tran.attrib['type'],
                                                symbol  = tran.attrib['symbol'],
                                                state   = int(tran.attrib['state']))
                    t_state[t_transition.symbol] = t_transition
            except Exception:
                raise XmlDecodeError, "On automaton. May have reduce/reduce confict. Please using bison compatible xml file."
            try:
                reductions = actions.find('reductions')
                for redu in reductions:
                    t_transition = Transition(  type    = "reduce",
                                                symbol  = redu.attrib['symbol'],
                                                rule    = redu.attrib['rule'])
                    if redu.attrib['enabled'] == 'true':
                        t_state[t_transition.symbol] = t_transition
            except Exception:
                raise XmlDecodeError, "On automaton. May have shift/reduce confict. Please using bison compatible xml file."
            self.automaton.append(t_state)
        return

    def state_transit(self, token):
        symbol = token.token_type
        while True:
            # print ("")
            # print (self.state_stack)
            # print (self.symbol_stack)
            state = self.state_stack[len(self.state_stack) - 1]
            transitions = self.automaton[state]

            try:
                if transitions[symbol].type == "shift": # shift and go
                    self.state_stack.append(transitions[symbol].state)
                    self.symbol_stack.append(symbol)
                    # 终结符语法分析元素
                    self.syntax_stack.append(self.syntaxer.token_to_terminal(token))
                    return
                elif transitions[symbol].type == "reduce": # reduce and go
                    if transitions[symbol].rule == "accept":
                        return
                    rule = self.rules[int(transitions[symbol].rule)]
                    rhs = []
                    for i in xrange(len(rule.rhs)):
                        if self.symbol_stack.pop() != rule.rhs[len(rule.rhs) - 1 - i]:
                            raise ParseringError(token, state)
                        self.state_stack.pop()
                        # 构建语法分析器传入参数
                        rhs.append(self.syntax_stack.pop())
                    # 归约处理部分
                    rhs = rhs[::-1]
                    rhs = tuple(rhs)
                    res = self.syntaxer.get_reduce_process_function(rule.number)(rhs)
                    # 符号栈
                    self.symbol_stack.append(rule.lhs)
                    # 语法栈
                    self.syntax_stack.append(res)
                    # 归约处理完成
                    t_state = self.state_stack[len(self.state_stack) - 1]
                    t_transitions = self.automaton[t_state]
                    try:
                        if t_transitions[rule.lhs].type == "goto":
                            self.state_stack.append(t_transitions[rule.lhs].stathe)
                        else:
                            raise ParseringError(token, state)
                    except Exception:
                        raise ParseringError(token, state)

            except KeyError: # reduce and go of $default
                try:
                    if transitions["$default"].type != "reduce":
                        self.syntaxer.error_handler(token, state)
                        raise ParseringError(token, state)
                    if transitions["$default"].rule == "accept":
                        return
                    rule = self.rules[int(transitions["$default"].rule)]
                    rhs = []

                    for i in xrange(len(rule.rhs)):
                        if self.symbol_stack.pop() != rule.rhs[len(rule.rhs) - 1 - i]:
                            raise ParseringError(token, state)
                        self.state_stack.pop()
                        # 构建语法分析器传入参数
                        rhs.append(self.syntax_stack.pop())

                    # 归约处理部分
                    rhs = rhs[::-1]
                    rhs = tuple(rhs)
                    res = self.syntaxer.get_reduce_process_function(rule.number)(rhs)

                    # 符号栈
                    self.symbol_stack.append(rule.lhs)
                    # 语法栈
                    self.syntax_stack.append(res)
                    # 归约处理结束
                    t_state = self.state_stack[len(self.state_stack) - 1]
                    t_transitions = self.automaton[t_state]
                    try:
                        if t_transitions[rule.lhs].type == "goto":
                            self.state_stack.append(t_transitions[rule.lhs].state)
                        else:
                            self.syntaxer.error_handler(token, state)
                            raise ParseringError(token, state)
                    except Exception:
                        raise ParseringError(token, state)
                except Exception, e:
                    # print ("")
                    # print (self.state_stack)
                    # print (self.symbol_stack)
                    raise ParseringError(token, state)
            except Exception, e:
                raise ParseringError(token, state)


    def parser(self, scanner, token_class, syntaxer):
        self.state_stack.append(0)
        self.scanner = scanner
        self.token_class = token_class
        self.syntaxer = syntaxer
        for each_token in scanner:
            try:
                self.state_transit(each_token)
            except Exception, e:
                print("")
                self.syntaxer.error_handler(e.token, e.state)
                return
            else:
                pass
            finally:
                pass
        token = token_class()
        token.token_type = "$end"
        self.state_transit(token)
        return

