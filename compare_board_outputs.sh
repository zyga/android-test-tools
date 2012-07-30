#!/bin/sh

compare_logs() {
	tmpfile_base=$(mktemp)
	tmpfile_other=$(mktemp)

	echo "Comparing $1 and $2..."
 
	cat $1 | cut -d '/' -f 7 > $tmpfile_base
	cat $2 | cut -d '/' -f 7 > $tmp_file_other
	diff -u --label $1 $tmpfile_base --label $2 $tmpfile_other
	rm -f $tmpfile_base $tmpfile_other
}

if [ $# != 2 ]; then
	echo "Usage: compare_board_output.sh  <product1> <product2>"
	exit 1
fi

base_uri_apks=extra-apks
base_uri_execs=extra-execs
base_uri_tests=common-test-execs

compare_logs ${base_uri_apks}-$1.txt ${base_uri_apks}-$2.txt
compare_logs ${base_uri_execs}-$1.txt ${base_uri_execs}-$2.txt
compare_logs ${base_uri_tests}-$1.txt ${base_uri_tests}-$2.txt
