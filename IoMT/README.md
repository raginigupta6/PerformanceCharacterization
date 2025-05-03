


nano kmeans.c
g++  kmeans.c -o kmeans.o
g++  kmeans.c -o kmeans.o
docker build -t kmeans_cont .	
perf stat docker run kmeans_cont 

on host:
per stat -B -e cache-references,cache-misess,cycles,instructions,branches,faults,migrations ./kmeans.o
perf stat -B -e cache-misses,cycles,instructions,branches,faults,migrations ./kmeans.o
perf stat -B -e cache-misses,cycles,instructions,branches,faults,migrations docker run kmeans_cont


nano lzw.cpp
g++ lzw.cpp -o lzw.o
docker build -t lzw_cont .
perf stat -B -e cache-misses,cycles,instructions,branches,faults,migrations docker run lzw_cont

nano lzw.cpp
g++ lzw.cpp -o lzw.o
perf stat -B -e cache-misses,cycles,instructions,branches,faults,migrations ./lzw.o


dd if=/dev/urandom of=test.txt bs=1M count=1
dd if=/dev/urandom of=test.txt bs=10M count=1
dd if=/dev/urandom of=test.txt bs=100M count=1
perf stat -B -e cache-misses,cycles,instructions,branches,faults,migrations ./aesExampleBin



