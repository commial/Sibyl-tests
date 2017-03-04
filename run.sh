#!/bin/bash
NOBUF="stdbuf -oL -eL"
set -e
set -o pipefail

function run_test {
	NAME=$1
	EXTRA_ARGS=$2

	RESULT=$name\_result
	($NOBUF sibyl find $EXTRA_ARGS binaries/$NAME $(cat addresses/$NAME\_addr) 2>&1 || echo 'Fail' 1>&2) | $NOBUF grep -Ev '(WARNING|access to non writable page)' | tee $RESULT

	echo "********************************************************************************"
	sort $RESULT -o $RESULT
	diff -u expected/$NAME\_expected $RESULT || true
	echo "********************************************************************************"
	rm $RESULT
}

echo "********************************************************************************"
echo "Run x86_32 tests..."
echo "********************************************************************************"

# Basic behavior
run_test libc-2.21.so '-a x86_32 -b ABIStdCall_x86_32'

# QEMU + autodetect of ARCH
run_test libc-2.21.so '-b ABIStdCall_x86_32 -j qemu'

echo "********************************************************************************"
echo "Run ARM L tests..."
echo "********************************************************************************"

# Basic behavior
run_test busybox-armv6l '-a arml'

# QEMU + autodetect of ABI + autodetect of ARCH
run_test busybox-armv6l '-j qemu'

echo "********************************************************************************"
echo "Run MIPS32 L tests..."
echo "********************************************************************************"

# Basic behavior
run_test busybox-mipsel '-a mips32l -b ABI_MIPS_O32'

# autodetect of ABI + autodetect of ARCH
run_test busybox-mipsel

echo "********************************************************************************"
echo "Run LEARN tests..."
echo "********************************************************************************"
cd learned_binaries
python run_learn_tests.py 2> /dev/null
cd ..
echo "********************************************************************************"
