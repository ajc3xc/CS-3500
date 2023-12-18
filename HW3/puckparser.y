/********************************************************
 * hint.y
 ********************************************************/
// -- PREAMBLE ------------------------------------------
%{
#include <iostream>
using namespace std;

  // Things from Flex that Bison needs to know
extern int yylex();
extern int line_num;
extern char* yytext;

  // Prototype for Bison's error message function
int yyerror(const char *p);

  //Prototype for output message function 
void print_statement(string rule_type, string specific_word);
%}

//-- TOKEN DEFINITIONS --
// what tokens to expect from Flex

%token K_IF
%token K_FUNCTION
%token K_THEN
%token K_ELSE
%token K_FI
%token K_SC
%token K_LPAREN
%token K_RPAREN
%token K_WRITE
%token K_LOOP
%token K_POOL
%token K_DO

%token OP_ASSIGN
%token OP_MULT
%token OP_NEG
%token OP_RELATION
%token OP_ADD

%token T_IDENT
%token T_INTEGER
%token T_DECIMAL
%token T_STRING


%%

//-- GRAMMAR RULES ------------------------------------
/* NOTE: Bison likes the start symbol to be the first rule */
/* NOTE TO SELF: this is really complicated and you should probably think this over a bit
this is not going to be easy to think out and solve */

StatementSequence	:  Statement					{ print_statement("StatementSequence", "Statement"); }
			|  Statement K_SC StatementSequence		{ print_statement("StatementSequence", "Statement ; StatementSequence"); }
			;

Statement	:	Assignment		{ print_statement("Statement", "Assignment"); }
			|	WriteStatement	{ print_statement("Statement", "WriteStatement"); }
			|	IfStatement		{ print_statement("Statement", "IfStatement"); }
			|	LoopStatement	{ print_statement("Statement", "LoopStatement"); }

IfStatement	:	K_IF Expression K_THEN StatementSequence K_FI
				{ print_statement("IfStatement", "IF Expression THEN StatementSequence FI"); }
			|	K_IF Expression K_THEN StatementSequence K_ELSE StatementSequence K_FI 
				{ print_statement("IfStatement", "IF Expression THEN StatementSequence ELSE StatementSequence FI"); }
			;

LoopStatement	:	K_LOOP Expression K_DO StatementSequence K_POOL
					{ print_statement("LoopStatement", "LOOP Expression DO StatementSequence POOL"); }
			;

Assignment	:  T_IDENT OP_ASSIGN Expression	{ print_statement("Assignment", "identifier := Expression"); }
			;

WriteStatement	:  K_WRITE K_LPAREN Expression K_RPAREN { print_statement("WriteStatement", "WRITE ( Expression )"); }
			;

Expression 	:  SimpleExpression							{ print_statement("Expression", "SimpleExpression"); }
			|  SimpleExpression OP_RELATION Expression	{ print_statement("Expression", "SimpleExpression OP_RELATION Expression"); }
			;

SimpleExpression 	:  Term					{ print_statement("SimpleExpression", "Term"); }
			|  Term OP_ADD SimpleExpression	{ print_statement("SimpleExpression", "Term OP_ADD SimpleExpression"); }
			;

Term 	:	   Factor				{ print_statement("Term", "Factor"); }
			|  Factor OP_MULT Term	{ print_statement("Term", "Factor OP_MULT Term"); }
			;

Factor  :	   T_INTEGER	{ print_statement("Factor", "T_INTEGER"); }
			|  T_DECIMAL	{ print_statement("Factor", "T_DECIMAL"); }
			|  T_STRING		{ print_statement("Factor", "T_STRING"); } 
			|  T_IDENT		{ print_statement("Factor", "T_IDENT"); } 
			|  K_LPAREN Expression K_RPAREN { print_statement("Factor", "( Expression )"); }
			|  OP_NEG Factor { print_statement("Factor", "~Factor"); }
			;

%% //-- EPILOGUE ---------------------------------------------

/*
Assignment  :  T_IDENT OP_ASSIGN T_DECIMAL
               { cout << "RULE: Assignment ::= T_IDENT := T_DECIMAL" << endl; }
            ;

WriteStatement  :  K_WRITE K_LPAREN T_INTEGER K_RPAREN
                   { cout << "RULE: WriteStatement ::= WRITE ( T_INTEGER )" << endl; }
                ;
*/


//Function to help automate the basic ascepts of printing out statements
//This could probably be improved upon, but it's good enough to get the job done
void print_statement(string rule_type, string specific_word)
{
	cout << "RULE: " << rule_type << " ::= " << specific_word << endl;
}

// Bison error function 
int yyerror(const char *p)
{
  cout << "ERROR: In line " << line_num << " with token \'"
       << yytext << "\'" << endl;
  return 0;
}

int main()
{
  int failcode;
  failcode = yyparse();

  if (failcode)
    cout << "INVALID!" << endl;
  else
    cout << "CORRECT" << endl;
  return 0;
}
