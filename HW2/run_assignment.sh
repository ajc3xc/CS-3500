#!/bin/bash

set -Eeo pipefail

#remove files if they exist
[ -f lex.yy.c ] && rm lex.yy.c
[ -f lexer.ex ] && rm lexer.ex

#generate compiled files, run program
#flex mylexer.l
flex mylexer.l
g++ lex.yy.c -lfl -o lexer.ex
./lexer.ex < input.txt

#remove files if they exist
[ -f lex.yy.c ] && rm lex.yy.c
[ -f lexer.ex ] && rm lexer.ex