#!/usr/bin/env bash

#mkdir -p experimental-results-f32
#for input in $(echo experimental-data/s*)
#do
#	input_without_extension="${input%.txt}"
#	filename="${input_without_extension#experimental-data/}"
#	echo "$filename"
#	./tp.f32 "$input" "experimental-results-f32/${filename}.cmm" 0
#	./tp.f32 "$input" "experimental-results-f32/${filename}.wp" 1
#	./tp.f32 "$input" "experimental-results-f32/${filename}.justice" 2
#	./tp.f32 "$input" "experimental-results-f32/${filename}.elo" 3
#done

mkdir -p experimental-results-f64
for input in $(echo experimental-data/s*)
do
	input_without_extension="${input%.txt}"
	filename="${input_without_extension#experimental-data/}"
	echo "$filename"
	./tp.f64 "$input" "experimental-results-f64/${filename}.cmm" 0
	./tp.f64 "$input" "experimental-results-f64/${filename}.wp" 1
	./tp.f64 "$input" "experimental-results-f64/${filename}.justice" 2
	./tp.f64 "$input" "experimental-results-f64/${filename}.elo" 3
done

#mkdir -p experimental-results-f80
#for input in $(echo experimental-data/s*)
#do
#	input_without_extension="${input%.txt}"
#	filename="${input_without_extension#experimental-data/}"
#	echo "$filename"
#	./tp.f80 "$input" "experimental-results-f80/${filename}.cmm" 0
#	./tp.f80 "$input" "experimental-results-f80/${filename}.wp" 1
#	./tp.f80 "$input" "experimental-results-f80/${filename}.justice" 2
#	./tp.f80 "$input" "experimental-results-f80/${filename}.elo" 3
#done
