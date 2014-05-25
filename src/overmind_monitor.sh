#!/bin/bash
Cmd="./overmind_logger"
Log="./samples/overmind.csv"
Dev="/dev/rfcomm0"


echo "x,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11"  > $Log
echo "seconds, signals, attention, meditation, delta, theta, low alpha, high alpha, low beta, high beta, low gamma, high gamma"  >>$Log
n=0

#$Cmd $n $Dev > $Log


while [ 1 ]; do
	$Cmd $n $Dev >>$Log
#	echo $Cmd $n $Dev
#        `$Cmd $n $Dev` 2>&1  |    while read line; do
#					echo  $line >> $Log
#	done
	(( n++ ))
	sleep 1
done
