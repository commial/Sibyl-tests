#!/bin/sh
echo "********************************************************************************"
echo "Run ARM L tests..."
echo "********************************************************************************"

python $SIBYL/find.py binaries/busybox-armv6l arml ABI_ARM $(cat addresses/busybox-armv6l_addr) -q 2>&1 | grep -v "WARNING: " | grep -v "access to non writable page" | sort | tee busybox-armv6l_result

echo "********************************************************************************"
diff -u expected/busybox-armv6l_expected  busybox-armv6l_result
echo "********************************************************************************"
rm busybox-armv6l_result


echo "********************************************************************************"
echo "Run MIPS32 L tests..."
echo "********************************************************************************"

python $SIBYL/find.py binaries/busybox-mipsel mips32l ABI_MIPS_O32 $(cat addresses/busybox-mipsel_addr) -q 2>&1 | grep -v "WARNING: " | grep -v "access to non writable page" | sort | tee busybox-mipsel_result

echo "********************************************************************************"
diff -u expected/busybox-mipsel_expected  busybox-mipsel_result
echo "********************************************************************************"
rm busybox-mipsel_result
