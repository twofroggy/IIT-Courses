#!/bin/bash
if [ $# != 1 ]
then
	echo "Arguments: [filename]"
	exit -1
fi

filename=$1

sort -n $filename > "$filename.sorted"
