#!/bin/sh
echo "********************************************************************************"
echo "Run x86_32 tests..."
echo "********************************************************************************"

python $SIBYL/find.py -q -a x86_32 binaries/libc-2.21.so ABIStdCall_x86_32 $(cat addresses/libc-2.21_addr) 2>&1 | grep -v "WARNING " | grep -v "access to non writable page" | sort | tee libc-2.21_result

echo "********************************************************************************"
diff -u expected/libc-2.21_expected  libc-2.21_result
echo "********************************************************************************"
rm libc-2.21_result

python $SIBYL/find.py -q binaries/libc-2.21.so ABIStdCall_x86_32 2>&1 | grep -v "WARNING " | grep -v "access to non writable page" | sort | tee libc-2.21_result

echo "********************************************************************************"
diff -u expected/libc-2.21_expected  libc-2.21_result
echo "********************************************************************************"
rm libc-2.21_result

echo "********************************************************************************"
echo "Run ARM L tests..."
echo "********************************************************************************"

python $SIBYL/find.py -a arml -q binaries/busybox-armv6l ABI_ARM $(cat addresses/busybox-armv6l_addr) 2>&1 | grep -v "WARNING " | grep -v "access to non writable page" | sort | tee busybox-armv6l_result

echo "********************************************************************************"
diff -u expected/busybox-armv6l_expected  busybox-armv6l_result
echo "********************************************************************************"
rm busybox-armv6l_result

python $SIBYL/find.py -q binaries/busybox-armv6l ABI_ARM 2>&1 | grep -v "WARNING " | grep -v "access to non writable page" | sort | tee busybox-armv6l_result

echo "********************************************************************************"
diff -u expected/busybox-armv6l_expected  busybox-armv6l_result
echo "********************************************************************************"
rm busybox-armv6l_result


echo "********************************************************************************"
echo "Run MIPS32 L tests..."
echo "********************************************************************************"

python $SIBYL/find.py -a mips32l -q binaries/busybox-mipsel ABI_MIPS_O32 $(cat addresses/busybox-mipsel_addr) 2>&1 | grep -v "WARNING " | grep -v "access to non writable page" | sort | tee busybox-mipsel_result

echo "********************************************************************************"
diff -u expected/busybox-mipsel_expected  busybox-mipsel_result
echo "********************************************************************************"
rm busybox-mipsel_result

python $SIBYL/find.py -q binaries/busybox-mipsel ABI_MIPS_O32 2>&1 | grep -v "WARNING " | grep -v "access to non writable page" | sort | tee busybox-mipsel_result

echo "********************************************************************************"
diff -u expected/busybox-mipsel_expected  busybox-mipsel_result
echo "********************************************************************************"
rm busybox-mipsel_result
