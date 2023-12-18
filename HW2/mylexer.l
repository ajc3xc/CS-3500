/* A starting flex file */
		               /* ---- PROLOGUE ---- */
%{
#include <iostream>
using namespace std;

int lines_counter = 1; //The last line doesn't have \n, so needs to start at 1
int counter = 0;

//simple function to print the lexeme type
void print_lexeme(string token_type, string yytext)
{
	//calculate the number of spaces between token type and item
	//The output has the number of spaces as 12 - len(token_type), so I'm going to follow the exact same format
	int spaces = 12 - token_type.length();
	string cout_spaces(spaces, ' ');
	
	cout << counter << ": TOKEN: " <<  token_type << cout_spaces << "LEXEME: " << yytext << endl;
	counter++;
}

//STRLITERAL	\"[a-zA-Z0-9]+\"
//IDENTIFIER	<[^{KEYWORD}{HEXADECIMAL}{CHARLITERAL}]>[a-zA-Z][a-zA-Z0-9_]+

%}
		              /* ---- DEFINITIONS ---- */
%option noyywrap
DIGIT		[0-9]
ALPHABET	[a-zA-Z]
HEX_VAL		[{DIGIT}A-F]

INTEGER		[+-]?{DIGIT}+
DECIMAL		{INTEGER}[.]{DIGIT}+
SCIENTIFIC	{DECIMAL}[E][1-9]+
HEXADECIMAL	{HEX_VAL}+[H]
BINARY		[01]+[B]
KEYWORD		"FUNCTION"|"IF"|"FI"|"LOOP"|"POOL"|"PRINT"
QUOTE		\"
STRLITERAL	[\"][^ \n\t\r\"]*[\"]
CHARLITERAL	[0-9A-F]+[X]
IDENTIFIER	[a-zA-Z][a-zA-Z0-9_]*
OPERATOR	"+"|"-"|"*"|"/"|"<"|">"|"="|"&"|"#"
COMMENT		[%]+.*$
INVALID		[^{INTEGER}{DECIMAL}{SCIENTIFIC}{HEXADECIMAL}{SCIENTIFIC}{BINARY}{KEYWORD}{QUOTE}{STRLITERAL}{CHARLITERAL}{IDENTIFIER}{OPERATOR}{COMMENT}\r]


%%  		              /* ---- REGULAR EXPRESSIONS ---- */

[ \t]           ;
\n              { lines_counter++; }
{INTEGER}		{ print_lexeme("INTCONST", yytext); }
{DECIMAL}		{ print_lexeme("DECCONST", yytext); }
{SCIENTIFIC}	{ print_lexeme("SCICONST", yytext); }
{HEXADECIMAL}	{ print_lexeme("HEXCONST", yytext); }
{BINARY}		{ print_lexeme("BINCONST", yytext); }
{KEYWORD}		{ print_lexeme("KEYWORD", yytext); }
{STRLITERAL}	{ print_lexeme("STRCONST", yytext); }
{CHARLITERAL}	{ print_lexeme("CHCONST", yytext); }
{IDENTIFIER}	{ print_lexeme("IDENT", yytext); }
{OPERATOR}		{ print_lexeme("OPERATOR", yytext); }
{COMMENT}		{}
{INVALID}		{ print_lexeme("?", yytext); }


%%  		              /* ---- EPILOGUE ---- */

//some old tests I used. I don't feel like deleting them
//[a-zA-Z0-9]+    { cout << "Found a string: " << yytext << endl; }
//{COMMENT}		{ print_lexeme("COMMENT", yytext); }

int main()
{
    cout << "Hello FLEX!" << endl;
    yylex();
    cout << lines_counter << " lines processed." << endl;
    return 0;
}
