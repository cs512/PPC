#! /usr/bin/python
#coding: utf-8

class RedfineError(Exception):
    """docstring for ConstError"""
    def __init__(self, arg):
        Exception.__init__(self)
        self.arg = arg
        return

class NotDefineError(Exception):
    """docstring for NotDefineError"""
    def __init__(self, arg):
        Exception.__init__(self)
        self.arg = arg
        return

class AssignmentError(Exception):
    """docstring for AssignmentError"""
    def __init__(self, arg):
        Exception.__init__(self)
        self.arg = arg
        return

class CodeSet(object):
    """docstring for CodeSet"""
    def __init__(self):
        self.code_set = []
        return

    def add_code(self, op, l, a):
        self.code_set.append((op, l, a))
        return

    def get_length(self):
        # print (self.code_set)
        # print (len(self.code_set))
        return len(self.code_set)

    def append(self, code_set):
        for eachCode in code_set.code_set:
            self.code_set.append(eachCode)
        return self

class Variation(object):
    """docstring for Variation"""
    def __init__(self, type, value):
        super(Variation, self).__init__()
        self.type = type
        self.value = value

class BackEnd(object):
    """docstring for BackEnd"""

    def __init__(self, output):
        # self.const_table = {}
        # self.const_table_stack = []
        self.var_count = 3
        self.var_table = {}
        self.var_table_stack = []
        self.procedure_name_stack = []
        self.procedure_table = {}
        self.procedure_table_stack = []
        self.pcode_num = 0
        self.procedure_entracne_table = {}
        self.current_pos = 1
        self.buffer = []
        self.output = open(output, "w")

    def trigger_error(self, token, exception, message):
        raise exception, message

    def add_const(self, name, value):
        if name in self.var_table:
            print ("Const Redefine:" + str(name))
            raise RedfineError, "Const Redefine:" + str(name)
        # print ("CONST", name, value)
        var = Variation(0, value)
        self.var_table[name] = var
        return
    
    # def push_new_const_stack(self):
    #     self.const_table_stack.append(self.const_table)
    #     self.const_table = {}
    #     return

    # def pop_const_stack(self):
    #     return self.const_table_stack.pop()

    def pop_var_stack(self):
        return self.var_table_stack.pop()

    def push_new_var_stack(self):
        self.var_table_stack.append(self.var_table)
        self.var_table = {}
        self.var_count = 3
        return

    def add_var(self, name):
        if name in self.var_table:
            print ("Variation Redefine:" + str(name))
            raise RedfineError, "Variation Redefine:" + str(name)
        # print ("VAR", name, self.var_count)
        var = Variation(1, self.var_count)
        self.var_table[name] = var
        self.var_count += 1
        return

    def new_push_procedure_table_stack(self):
        self.procedure_table = {}
        self.procedure_table_stack.append(self.procedure_table)
        return

    def pop_procedure_table_stack(self):
        pop = self.procedure_table_stack.pop()
        return pop

    def add_procedure(self, name, uuid):
        if name in self.procedure_table:
            print ("Procedure Name Redefine:" + str(uuid))
            raise RedfineError, "Procedure Name Redefine:" + str(uuid)
        self.procedure_table_stack[len(self.procedure_table_stack) - 1][name] = uuid
        return

    def add_procedure_entrance(self, uuid, entrance):
        if uuid in self.procedure_name_stack:
            print ("Procedure Name Redefine:" + str(uuid))
            raise RedfineError, "Procedure Name Redefine:" + str(uuid)
        self.procedure_entracne_table[uuid] = entrance
        return

    # def generate_int(self):
    #     self.pcode_num += 1
    #     t_var_table = self.var_table_stack[len(self.var_table_stack) - 1]
    #     self.generate_code("INT", "0", len(t_var_table))
    #     return self.pcode_num - 1

    def push_procedure_name(self, name):
        self.procedure_name_stack.append(name)
        return

    def pop_procedure_name(self):
        return self.procedure_name_stack.pop()

    def generate_uuid(self):
        uuid = ""
        for x in self.procedure_name_stack:
            uuid += "{0}.".format(x)
        # print (uuid)
        return uuid

    def get_var(self, name):
        l = len(self.var_table_stack) - 1
        for i in xrange(l, -1, -1):
            if name in self.var_table_stack[i]:
                return (l - i, self.var_table_stack[i][name].value, self.var_table_stack[i][name].type)
        print ("Identifier Not Defined:" + str(name))
        raise NotDefineError, "Identifier Not Defined:" + str(name)
        return (-1, -1, -1)

    def get_procedure(self, name):
        l = len(self.procedure_table_stack) - 1
        for i in xrange(l, -1, -1):
            if name in self.procedure_table_stack[i]:
                return (l - i, self.procedure_table_stack[i][name])
        print ("Procedure Not Defined:" + str(name))
        raise NotDefineError, "Procedure Not Defined:" + str(name)
        return (-1, -1)

    def generate_code(self, code_set):
        for eachCode in code_set.code_set:
            self.buffer.append(eachCode)
            # self.output.write("{0}\n".format(eachCode))
            self.current_pos += 1
        return

    def layout_code(self, entrance):
        self.output.write("0: JMP 0 {0}\n".format(entrance))
        count = 1
        for eachCode in self.buffer:
            if eachCode[0] == "JMP":
                l = eachCode[1]
                a = eachCode[2] + count
                self.output.write("{0}: JMP 0 {1}\n".format(count, a))
                count += 1
            elif eachCode[0] == "JPC":
                l = eachCode[1]
                a = eachCode[2] + count
                self.output.write("{0}: JPC 0 {1}\n".format(count, a))
                count += 1
            elif eachCode[0] == "CALL":
                l = eachCode[1]
                a = self.procedure_entracne_table[eachCode[2]]
                self.output.write("{0}: CAL {1} {2}\n".format(count, l, a))
                count += 1
            else:
                self.output.write("{0}: {1} {2} {3}\n".format(count, eachCode[0], eachCode[1], eachCode[2]))
                count += 1
        return

    def get_current_pos(self):
        return self.current_pos

    def get_var_count(self):
        res = 3
        leng = len(self.var_table_stack) - 1
        for eachVar in self.var_table_stack[leng]:
            if self.var_table_stack[leng][eachVar].type == 1:
                res += 1
        return res

    def close(self):
        self.output.close()
        return
