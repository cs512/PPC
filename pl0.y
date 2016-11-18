%{ 
    #include <stdio.h> 
    #include <stdlib.h> 
 
    #include "calc_ast.h" 
 
    calc_ast* calc_result;
    int calc_eof = 0;
%} 
 
%union { 
    calc_ast *a;
    double d;
} 

%token IDENT CONST 
 
%% 
program	: block "." {print("begin");}
	;
block	: const_declaration var_declaration procedure_declarations statemente
	| const_declaration var_declaration statemente
	;

const_declaration	: 
			| "CONST" assignments ";"
			;
assignments	: IDENT "=" CONST
		| IDENT "=" CONST "," assignments
		;

var_declaration	:	
		| "VAR" idents ";"
		;
idents	: IDENT
	| IDENT "," idents
	;

procedure_declarations	: procedure_declaration
			| procedure_declaration procedure_declarations
			;
procedure_declaration	: procedure_head block ";"
			;
statemente	: 
		| statement
		;
statement	: IDENT ":=" expression
		| "CALL" IDENT
		| "BEGIN" statements "END"
		| "IF" condition "THEN" statemente
		| "IF" condition "THEN" statemente "ELSE" statemente
		| "WHILE" condition "DO" statemente
		| "READ" IDENT
		| "WRITE" expression
		| expression
		;
statements	: statemente
		| statemente ";" statements
		;
condition	: "ODD" expression
		| expression rel_op expression
		;

rel_op	: "="
	| "<>"
	| "<"
	| "<="
	| ">"
	| ">="
	;
add_op	: "+"
	| "-"
	;
mul_op	: "*"
	| "/"
	;
expression	: terms
		| add_op terms
		;
terms	: term
	| term add_op terms
	;
term	: factor
	| factor mul_op term
	;
factor	: IDENT
	| CONST
	| "(" expression ")"
	;
procedure_head	: "PROCEDURE" IDENT ";"
		;
%% 
 
int main (int argc, char** argv) {
    int i = 1;
 
    printf("Calc V0.1 from: http://unbe.cnnn");
 
    for (;;) {
        fprintf(stdout, "%d> ", i);
 
        if (!yyparse() && !calc_eof) {
            printf("%fn", calc_ast_eval(calc_result));
            calc_ast_free(calc_result);
            i ++;
        } else if (calc_eof) {
            break;
        } else {
            rewind(stdin);
            yyrestart(stdin);
        }
    }
    return 0;
}
 
yyerror (char *s) {
    fprintf(stderr, "error: %sn", s);
}

