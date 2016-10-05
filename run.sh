#!/bin/bash
NOBUF="stdbuf -oL -eL"
set -e
set -o pipefail

function run_test {
	NAME=$1
	ABI=$2
	EXTRA_ARGS=$3

	RESULT=$name\_result
	($NOBUF python $SIBYL/find.py -q $EXTRA_ARGS binaries/$NAME $ABI $(cat addresses/$NAME\_addr) 2>&1 || echo 'Fail' 1>&2) | $NOBUF grep -Ev '(WARNING|access to non writable page)' | tee $RESULT

	echo "********************************************************************************"
	sort $RESULT -o $RESULT
	diff -u expected/$NAME\_expected $RESULT || true
	echo "********************************************************************************"
	rm $RESULT
}

echo "********************************************************************************"
echo "Run x86_32 tests..."
echo "********************************************************************************"

run_test libc-2.21.so ABIStdCall_x86_32 '-a x86_32'

run_test libc-2.21.so ABIStdCall_x86_32

echo "********************************************************************************"
echo "Run ARM L tests..."
echo "********************************************************************************"

run_test busybox-armv6l ABI_ARM '-a arml'

run_test busybox-armv6l ABI_ARM

echo "********************************************************************************"
echo "Run MIPS32 L tests..."
echo "********************************************************************************"

run_test busybox-mipsel ABI_MIPS_O32 '-a mips32l'

run_test busybox-mipsel ABI_MIPS_O32

echo "********************************************************************************"
echo "Run LEARN tests..."
echo "********************************************************************************"
cd learned_binaries
python run_learn_tests.py 2> /dev/null
cd ..
echo "********************************************************************************"
