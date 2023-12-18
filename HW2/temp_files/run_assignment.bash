#!/bin/bash

set -Eeo pipefail

#remove files if they exist
[ -f lex.yy.c ] && rm lex.yy.c
[ -f lexer.ex ] && rm lexer.ex

cat input.txt
exit 1

#generate compiled files, run program
flex mylexer.l
g++ lex.yy.c -lfl -o lexer.ex
./lexer.ex < input.txt
