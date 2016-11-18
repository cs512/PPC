#! /usr/bin/python
#coding: utf-8

# import backend.BackEnd as BackEnd

from backend import BackEnd, CodeSet, AssignmentError
import ctypes

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE= -11
STD_ERROR_HANDLE = -12

FOREGROUND_BLACK = 0x0
FOREGROUND_BLUE = 0x01 # text color contains blue.
FOREGROUND_GREEN= 0x02 # text color contains green.
FOREGROUND_RED = 0x04 # text color contains red.
FOREGROUND_INTENSITY = 0x08 # text color is intensified.

BACKGROUND_BLUE = 0x10 # background color contains blue.
BACKGROUND_GREEN= 0x20 # background color contains green.
BACKGROUND_RED = 0x40 # background color contains red.
BACKGROUND_INTENSITY = 0x80 # background color is intensified.

backend = None

class Program(object):
    """docstring for Program"""
    def __init__(self):
        pass

class Block(object):
    """docstring for Block"""
    def __init__(self, entrance):
        self.entrance = entrance
        return

class ConstDeclaration(object):
    """docstring for ConstDeclaration"""
    def __init__(self):
        pass

class Assignments(object):
    """docstring for Assignments"""
    def __init__(self):
        pass

class VarDeclaration(object):
    """docstring for VarDeclaration"""
    def __init__(self):
        pass

class Idents(object):
    """docstring for Idents"""
    def __init__(self):
        pass

class ProcedureDeclarations(object):
    """docstring for ProcedureDeclarations"""
    def __init__(self):
        pass

class ProcedureDeclaration(object):
    """docstring for ProcedureDeclaration"""
    def __init__(self):
        return

class Statemente(object):
    """docstring for Statemente"""
    def __init__(self, code_set):
        self.code_set = code_set
        return

class Statement(object):
    """docstring for Statement"""
    def __init__(self, code_set):
        self.code_set = code_set
        return

class Statements(object):
    """docstring for Statements"""
    def __init__(self, code_set):
        self.code_set = code_set
        return

class Condition(object):
    """docstring for Condition"""
    def __init__(self, code_set):
        self.code_set = code_set
        return

class RelOp(object):
    """docstring for RelOp"""
    def __init__(self, type):
        self.type = type
        return

class AddOp(object):
    """docstring for AddOp"""
    def __init__(self, type):
        self.type = type
        return

class MulOp(object):
    """docstring for MulOp"""
    def __init__(self, type):
        self.type = type
        return

class Expression(object):
    """docstring for Expression"""
    def __init__(self, code_set):
        self.code_set = code_set
        return

class Terms(object):
    """docstring for Terms"""
    def __init__(self, code_set):
        self.code_set = code_set
        return

class Term(object):
    """docstring for Term"""
    def __init__(self, code_set):
        self.code_set = code_set
        return

class Factor(object):
    """docstring for Factor"""
    def __init__(self, code_set):
        self.code_set = code_set
        return

class ProcedureHead(object):
    """docstring for ProcedureHead"""
    def __init__(self, uuid):
        self.uuid = uuid

class Syntaxer(object):
    """docstring for Syntaxer"""
    std_out_handle = None
    # ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    def __init__(self, back_end):
        global backend
        backend = back_end

    def set_cmd_color(self, color, handle=std_out_handle):
        """(color) -> bit
        Example: set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY)
        """
        # bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        # return bool
        return True

    def reset_color(self):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
        return

    def token_to_terminal(self, token):
        return token

    def get_reduce_process_function(self, num):
        res = None
        exec("res = self.rule_{0}".format(num))
        # exec("res = self.rule_0")
        return res

    def error_handler(self, token, state):
        self.set_cmd_color(BACKGROUND_RED | BACKGROUND_GREEN | BACKGROUND_BLUE | FOREGROUND_RED | FOREGROUND_INTENSITY)
        print ("Error on {0}:{1}, State:{2}".format(token.row, token.col, state))
        self.reset_color()
        return

    def rule_0(self, rhs):
        """ $accept: program $end """
        return "$accept"

    def rule_1(self, rhs):
        """ program: block "." """
        program = Program()
        # print (backend.procedure_entracne_table)
        backend.layout_code(rhs[0].entrance)
        return program

    def rule_2(self, rhs):
        """ block: const_declaration var_declaration procedure_declarations statement """
        block = Block(backend.get_current_pos())
        code_set = CodeSet()
        code_set.add_code("INT", 0, backend.get_var_count())
        code_set.append(rhs[3].code_set)
        code_set.add_code("OPR", 0, 0)
        backend.generate_code(code_set)
        backend.pop_var_stack()
        backend.pop_procedure_table_stack()
        # print ""
        return block

    def rule_3(self, rhs):
        """ block: const_declaration var_declaration statement """
        block = Block(backend.get_current_pos())
        code_set = CodeSet()
        code_set.add_code("INT", 0, backend.get_var_count())
        code_set.append(rhs[2].code_set)
        code_set.add_code("OPR", 0, 0)
        backend.generate_code(code_set)
        backend.pop_var_stack()
        backend.pop_procedure_table_stack()
        # print ""
        return block

    def rule_4(self, rhs):
        """ const_declaration: /* empty */ """
        const_declaration = ConstDeclaration()
        return const_declaration

    def rule_5(self, rhs):
        """ const_declaration: "CONST" assignments ";" """
        const_declaration = ConstDeclaration()
        return const_declaration

    def rule_6(self, rhs):
        """ assignments: IDENT "=" CONST """
        backend.add_const(rhs[0].content, int(rhs[2].content))
        assignments = Assignments()
        return assignments

    def rule_7(self, rhs):
        """ assignments: IDENT "=" CONST "," assignments """
        backend.add_const(rhs[0].content, int(rhs[2].content))
        assignments = Assignments()
        return assignments

    def rule_8(self, rhs):
        """ var_declaration: /* empty */ """
        var_declaration = VarDeclaration()
        backend.push_new_var_stack()
        backend.new_push_procedure_table_stack()
        return var_declaration

    def rule_9(self, rhs):
        """ var_declaration: "VAR" idents ";" """
        var_declaration = VarDeclaration()
        backend.push_new_var_stack()
        backend.new_push_procedure_table_stack()
        return var_declaration

    def rule_10(self, rhs):
        """ idents: IDENT """
        idents = Idents()
        backend.add_var(rhs[0].content)
        return idents

    def rule_11(self, rhs):
        """ idents: IDENT "," idents """
        idents = Idents()
        backend.add_var(rhs[0].content)
        return idents

    def rule_12(self, rhs):
        """ procedure_declarations: procedure_declaration """
        procedure_declarations = ProcedureDeclarations()
        return procedure_declarations

    def rule_13(self, rhs):
        """ procedure_declarations: procedure_declaration procedure_declarations """
        procedure_declarations = ProcedureDeclarations()
        return procedure_declarations

    def rule_14(self, rhs):
        """ procedure_declaration: procedure_head block ";" """
        backend.add_procedure_entrance(rhs[0].uuid, rhs[1].entrance)
        procedure_declaration = ProcedureDeclaration()
        backend.pop_procedure_name()
        return procedure_declaration

    def rule_49(self, rhs):
        """ procedure_head: "PROCEDURE" IDENT ";" """
        backend.push_procedure_name(rhs[1].content)
        uuid = backend.generate_uuid()
        backend.add_procedure(rhs[1].content, uuid)
        procedure_head = ProcedureHead(uuid)
        return procedure_head

    def rule_15(self, rhs):
        """ statemente: /* empty */ """
        code_set = CodeSet()
        statemente = Statemente(code_set)
        return statemente

    def rule_16(self, rhs):
        """ statemente: statement """
        code_set = rhs[0].code_set
        statemente = Statemente(code_set)
        return statemente

    def rule_17(self, rhs):
        """ statement: IDENT ":=" expression """
        code_set = rhs[2].code_set
        l, a, t = backend.get_var(rhs[0].content)
        if t == 1:
            code_set.add_code("STO", l, a)
        else:
            backend.trigger_error(rhs[0], AssignmentError, "Const Is Not Assignable")
        statement = Statement(code_set)
        return statement

    def rule_18(self, rhs):
        """ statement: "CALL" IDENT """
        code_set = CodeSet()
        l, a = backend.get_procedure(rhs[1].content)
        code_set.add_code("CALL", l, a)
        statement = Statement(code_set)
        return statement

    def rule_19(self, rhs):
        """ statement: "BEGIN" statements "END" """
        statement = Statement(rhs[1].code_set)
        return statement

    def rule_20(self, rhs):
        """ statement: "IF" condition "THEN" statemente """
        code_set = rhs[1].code_set
        leng = rhs[3].code_set.get_length()
        code_set.add_code("JPC", 0, leng + 1)
        code_set.append(rhs[3].code_set)
        statement = Statement(code_set)
        return statement

    def rule_21(self, rhs):
        """ statement: "IF" condition "THEN" statemente "ELSE" statemente """
        code_set = rhs[1].code_set
        leng = rhs[3].code_set.get_length()
        code_set.add_code("JPC", 0, leng + 2)
        code_set.append(rhs[3].code_set)
        leng = rhs[5].code_set.get_length()
        code_set.add_code("JMP", 0, leng + 1)
        code_set.append(rhs[5].code_set)
        statement = Statement(code_set)
        return statement

    def rule_22(self, rhs):
        """ statement: "WHILE" condition "DO" statemente """
        code_set = rhs[1].code_set
        leng = rhs[3].code_set.get_length()
        code_set.add_code("JPC", 0, leng + 2)
        code_set.append(rhs[3].code_set)
        leng = code_set.get_length()
        code_set.add_code("JMP", 0, -leng)
        statement = Statement(code_set)
        return statement

    def rule_23(self, rhs):
        """ statement: "READ" IDENT """
        code_set = CodeSet()
        code_set.add_code("OPR", 0, 16)
        l, a, t = backend.get_var(rhs[1].content)
        if t == 1:
            code_set.add_code("STO", l, a)
        else:
            backend.trigger_error(rhs[1], AssignmentError, "Const Is Not Assignable")

        statement = Statement(code_set)
        return statement

    def rule_24(self, rhs):
        """ statement: "WRITE" expression """
        code_set = rhs[1].code_set
        code_set.add_code("OPR", 0, 14)
        code_set.add_code("OPR", 0, 15)
        statement = Statement(code_set)
        return statement

    def rule_25(self, rhs):
        """ statement: expression """
        statement = Statement(rhs[1].code_set)
        return statement

    def rule_26(self, rhs):
        """ statements: statemente """
        statements = Statements(rhs[0].code_set)
        return statements

    def rule_27(self, rhs):
        """ statements: statemente ";" statements """
        code_set = rhs[0].code_set
        code_set.append(rhs[2].code_set)
        statements = Statements(code_set)
        return statements

    def rule_28(self, rhs):
        """ condition: "ODD" expression """
        code_set = rhs[1].code_set
        code_set.add_code("OPR", 0, 6)
        condition = Condition(code_set)
        return condition

    def rule_29(self, rhs):
        """ condition: expression rel_op expression """
        code_set = rhs[0].code_set
        code_set.append(rhs[2].code_set)
        code_set.add_code("OPR", 0, rhs[1].type)
        condition = Condition(code_set)
        return condition

    def rule_30(self, rhs):
        """ rel_op: "=" """
        rel_op = RelOp(8)
        return rel_op

    def rule_31(self, rhs):
        """ rel_op: "<>" """
        rel_op = RelOp(9)
        return rel_op

    def rule_32(self, rhs):
        """ rel_op: "<" """
        rel_op = RelOp(10)
        return rel_op

    def rule_33(self, rhs):
        """ rel_op: "<=" """
        rel_op = RelOp(13)
        return rel_op

    def rule_34(self, rhs):
        """ rel_op: ">" """
        rel_op = RelOp(12)
        return rel_op

    def rule_35(self, rhs):
        """ rel_op: ">=" """
        rel_op = RelOp(11)
        return rel_op

    def rule_36(self, rhs):
        """ add_op: "+" """
        add_op = AddOp(2)
        return add_op

    def rule_37(self, rhs):
        """ add_op: "-" """
        add_op = AddOp(3)
        return add_op

    def rule_38(self, rhs):
        """ mul_op: "*" """
        mul_op = MulOp(4)
        return mul_op

    def rule_39(self, rhs):
        """ mul_op: "/" """
        mul_op = MulOp(5)
        return mul_op

    def rule_40(self, rhs):
        """ expression: terms """
        expression = Expression(rhs[0].code_set)
        return expression

    def rule_41(self, rhs):
        """ expression: add_op terms """
        expression = Expression(rhs[1].code_set)
        if rhs[0].type == 3:
            expression.code_set.add_code("OPR", 0, 1)
        return expression

    def rule_42(self, rhs):
        """ terms: term """
        terms = Terms(rhs[0].code_set)
        return terms

    def rule_43(self, rhs):
        """ terms: term add_op terms """
        code_set = rhs[0].code_set
        code_set.append(rhs[2].code_set)
        code_set.add_code("OPR", 0, rhs[1].type)
        terms = Terms(code_set)
        return terms

    def rule_44(self, rhs):
        """ term: factor """
        term = Term(rhs[0].code_set)
        return term

    def rule_45(self, rhs):
        """ term: factor mul_op term """
        code_set = rhs[0].code_set
        code_set.append(rhs[2].code_set)
        code_set.add_code("OPR", 0, rhs[1].type)
        term = Term(code_set)
        return term

    def rule_46(self, rhs):
        """ factor: IDENT """
        code_set = CodeSet()
        l, a, t = backend.get_var(rhs[0].content)
        if t == 1:
            code_set.add_code("LOD", l, a)
        else:
            code_set.add_code("LIT", 0, a)
        factor = Factor(code_set)
        return factor

    def rule_47(self, rhs):
        """ factor: CONST """
        code_set = CodeSet()
        code_set.add_code("LIT", 0, int(rhs[0].content))
        factor = Factor(code_set)
        return factor

    def rule_48(self, rhs):
        """ factor: "(" expression ")" """
        factor = Factor(rhs[1].code_set)
        return factor

