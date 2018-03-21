#!/usr/bin/env bash

#
# Script to benchmark system and get parameters needed to form cloud vector.
# Ex: sudo ./a2cloud-bench.sh AWS t2large
#
#

PROVIDER=$1
INSTANCE_TYPE=$2

BENCH_DIR=$(pwd)

# compile everything
cd $BENCH_DIR
make &> /dev/null

# run benchmarks
RESULTS_DIR=${BENCH_DIR}/${PROVIDER}_${INSTANCE_TYPE}_BENCH_$(date +%Y%m%d_%H%M%S)
mkdir $RESULTS_DIR
cat /proc/cpuinfo > $RESULTS_DIR/cpuinfo.txt
echo "========================================================================================================"
echo "==                                          BEGIN LINPACK                                             =="
echo "========================================================================================================"
echo ""
cd $BENCH_DIR/LINPACK
for ((i=0;i<10;++i)); do
    ./linpacks.exe >> $RESULTS_DIR/linpacks.txt;
done
cat $RESULTS_DIR/linpacks.txt \
    |grep -E '[0-9]\.[0-9]{3}E(\+|\-)[0-9]{2}' \
    |awk '{ total += $4 } END { print total/NR " SP MFLOPS" }' \
    |tee -a $RESULTS_DIR/vector.txt
for ((i=0;i<10;++i)); do
    ./linpacks_x87.exe >> $RESULTS_DIR/linpacks_x87.txt
done
cat $RESULTS_DIR/linpacks_x87.txt \
    |grep -E '[0-9]\.[0-9]{3}E(\+|\-)[0-9]{2}' \
    |awk '{ total += $4 } END { print total/NR " x87 SP MFLOPS" }' \
    |tee -a $RESULTS_DIR/vector.txt
for ((i=0;i<10;++i)); do
    ./linpackd.exe >> $RESULTS_DIR/linpackd.txt
done
cat $RESULTS_DIR/linpackd.txt \
    |grep -E '[0-9]\.[0-9]{3}E(\+|\-)[0-9]{2}' \
    |awk '{ total += $4 } END { print total/NR " DP MFLOPS" }' \
    |tee -a $RESULTS_DIR/vector.txt
for ((i=0;i<10;++i)); do
    ./linpackd_x87.exe >> $RESULTS_DIR/linpackd_x87.txt
done
cat $RESULTS_DIR/linpackd_x87.txt \
    |grep -E '[0-9]\.[0-9]{3}E(\+|\-)[0-9]{2}' \
    |awk '{ total += $4 } END { print total/NR " x87 DP MFLOPS" }' \
    |tee -a $RESULTS_DIR/vector.txt
echo ""
echo "========================================================================================================"
echo "==                                          BEGIN STREAM                                              =="
echo "========================================================================================================"
echo ""
cd $BENCH_DIR/STREAM
./stream_c.exe > $RESULTS_DIR/stream.txt
cat $RESULTS_DIR/stream.txt \
    |grep -E '(Copy:|Scale:|Add:|Triad:)[[:space:]]+[0-9]+.[0-9]' \
    |awk '{ total += $2 } END { print total/NR " MEM MB/s" }' \
    |tee -a $RESULTS_DIR/vector.txt
echo ""
echo "========================================================================================================"
echo "==                                         BEGIN DD Test                                              =="
echo "========================================================================================================"
echo ""
echo 3 > /proc/sys/vm/drop_caches
for ((i=0;i<10;i++)); do
    sync; dd if=/dev/zero of=$BENCH_DIR/tempfile bs=1M count=1024 &>> $RESULTS_DIR/diskwrite.txt; sync
    echo 3 > /proc/sys/vm/drop_caches
    sync; dd if=$BENCH_DIR/tempfile of=/dev/null bs=1M count=1024 &>> $RESULTS_DIR/diskread.txt; sync;
    rm -rf $BENCH_DIR/tempfile
done
cat $RESULTS_DIR/diskwrite.txt \
    |& grep -E -o 's, [0-9]+.[0-9]+[[:space:]](MB/s|GB/s)' \
    |awk '{ total += $2 } END { print total/NR " DISK WRITE " $3 }' \
    |tee -a $RESULTS_DIR/vector.txt
cat $RESULTS_DIR/diskread.txt \
    |& grep -E -o 's, [0-9]+.[0-9]+[[:space:]](MB/s|GB/s)' \
    |awk '{ total += $2 } END { print total/NR " DISK READ " $3 }' \
    |tee -a $RESULTS_DIR/vector.txt