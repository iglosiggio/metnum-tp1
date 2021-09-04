#!/usr/bin/env bash

mkdir -p experimental-results

for input in $(echo experimental-data/s*)
do
	input_without_extension="${input%.txt}"
	filename="${input_without_extension#experimental-data/}"
	echo "$filename"
	./tp.f64 "$input" "experimental-results/${filename}.cmm" 0
	./tp.f64 "$input" "experimental-results/${filename}.wp" 1
	./tp.f64 "$input" "experimental-results/${filename}.justice" 2
	./tp.f64 "$input" "experimental-results/${filename}.elo" 3
done
