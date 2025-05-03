
[ "$(whoami)" == "root" ] || { echo "Must be run as sudo!"; exit 1; }



for (( mutex=1;  mutex<=100000;  mutex++ ))
do
	echo -e "*********"
	echo -e "Run $run"
	echo -e "*********\n"
	echo -e "Running CPU test...\n"

	sysbench --test=mutex --mutex-num=$mutex --thread-locks=5000000 --mutex-loops=1 run | grep 'total time:\|min:\|avg:\|max:' | tr -s [:space:]
	
	echo -e ""

done