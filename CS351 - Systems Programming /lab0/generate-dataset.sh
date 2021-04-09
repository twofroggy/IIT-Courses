#!/bin/bash 
if [ $# != 2 ]
then
	echo "Your file's name is [filename] and you have [num_records] records."
	exit -1
fi 

filename=$1
num_records=$2
tempint="$filename.ints"
tempstr="$filename.str"

for i in {1...num_records}; do
	echo $RANDOM $RANDOM > $tempint
done

base64 -w 100 /dev/urandom | head -n $num_records > $tempstr

paste $tempint $tempstr > $filename


