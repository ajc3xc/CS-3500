/* A starting flex file */
		               /* ---- PROLOGUE ---- */
%{
#include <iostream>
using namespace std;

int no_lines = 0;
%}
		              /* ---- DEFINITIONS ---- */
%option noyywrap
DIGIT		[0-9]

%%  		              /* ---- REGULAR EXPRESSIONS ---- */

[ \t]           ;
\n              { no_lines++; cout<<endl;}
{DIGIT}+        { cout << "Found an number: " << yytext << endl; }
[a-zA-Z0-9]+    { cout << "Found a string: " << yytext << endl; }



%%  		              /* ---- EPILOGUE ---- */

int main()
{
    cout << "Hello FLEX!" << endl;
    yylex();
    cout << "Done!" << endl;
    return 0;
}
