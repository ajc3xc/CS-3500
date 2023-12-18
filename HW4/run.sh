#!/bin/bash

set -Eeo pipefail

#iterate through all the lines and append each of them into a single string
all_lines=""
while read -r "line"
do
    #when * is loaded, it interprets it as a wildcard
    #which means it is replace with all the visible files in the directory
    #to fix this, I substituted the regex of the visible files with a regex
    #this is clumsy, but it works
    visible_dir=$(echo *)
    replacement="*"
    all_lines+=" ${line/visible_dir/replacement}"
    #echo "$all_lines"
done

#now that all the lines are in a single string, input it to the python file
python3 puckparser.py3 "$all_lines"