#!/bin/bash

#set -Eeo pipefail

i=1
for FILE in samples/*; do
    echo $FILE
    bash run.sh < $FILE
    echo
    ((i++))
done