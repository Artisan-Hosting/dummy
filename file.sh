for i in $(seq 1 100);
do
	mkdir ./$i
	for x in $(seq 1 1000)
	do
    	echo "random data" > ./$i/$x.rnd
    done
done
