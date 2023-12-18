#!/bin/bash

set -Eeo pipefail

#remove files if they exist (if not already deleted)
[ -f lex.yy.c ] && rm lex.yy.c
[ -f puckparser.ex ] && rm puckparser.ex
[ -f puckparser.tab.c ] && rm puckparser.tab.c
[ -f puckparser.tab.h ] && rm puckparser.tab.h
[ -f out.txt ] && rm out.txt

#run actual code
bison -d puckparser.y
flex puckparser.l
g++ puckparser.tab.c lex.yy.c -o puckparser.ex
#./puckparser.ex < hint_samples/hintsample2.txt
./puckparser.ex < samples/sample5.puk > out.txt 
diff out.txt samples/sample5out.txt

#remove files once finished running
[ -f lex.yy.c ] && rm lex.yy.c
[ -f puckparser.ex ] && rm puckparser.ex
[ -f puckparser.tab.c ] && rm puckparser.tab.c
[ -f puckparser.tab.h ] && rm puckparser.tab.h
[ -f out.txt ] && rm out.txt