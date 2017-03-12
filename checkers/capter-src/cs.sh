#!/bin/bash


function gen_flag(){
	flag=$(LC_ALL=C; cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 31; echo "=")
	flag_id=$(LC_ALL=C; cat /dev/urandom | tr -dc 'a-z0-9\-' | head -c 16)
}

OK=0
FAILED=0

function check() {
	while true; do
		echo "========== OK: $OK, FAILED: $FAILED ========="
		gtimeout 5 ./checker check localhost >/dev/null 2>&1
		ret=$?
		if [ $ret -ne 101 ]; then
			echo "CHECK FAILED: $ret"
			((FAILED+=1))
			sleep 1
			continue
		fi
		gen_flag
		gtimeout 5 ./checker put localhost "$flag_id" "$flag" 1 2>&1
		ret=$?
		if [ $ret -ne 101 ]; then
			echo "PUT FAILED: $flag_id - $ret"
			((FAILED+=1))
			sleep 1
			continue
		fi
		gtimeout 5 ./checker get localhost "$flag_id" "$flag" 1 2>&1
		ret=$?
		if [ $ret -ne 101 ]; then
			echo "GET FAILED: $flag_id - $ret"
			((FAILED+=1))
			sleep 1
			continue
		fi
		((OK+=1))
	done
}

check | ts | tee check.log