#!/bin/sh
sleep 20
while :
do
	echo "Running Python Script"
	python -u all_instances.py
	sleep 60
done