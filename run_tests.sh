#!/bin/bash
rm results
for value in ISOLATION_LEVEL_DEFAULT ISOLATION_LEVEL_AUTOCOMMIT ISOLATION_LEVEL_READ_COMMITTED ISOLATION_LEVEL_REPEATABLE_READ ISOLATION_LEVEL_SERIALIZABLE ISOLATION_LEVEL_READ_UNCOMMITTED
do
	echo $value >> results
	sed -i -e "s/ISOLATION_LEVEL_DEFAULT/$value/g" ./agent.py
	sed -i -e "s/ISOLATION_LEVEL_AUTOCOMMIT/$value/g" ./agent.py
	sed -i -e "s/ISOLATION_LEVEL_READ_COMMITTED/$value/g" ./agent.py
	sed -i -e "s/ISOLATION_LEVEL_REPEATABLE_READ/$value/g" ./agent.py
	sed -i -e "s/ISOLATION_LEVEL_SERIALIZABLE/$value/g" ./agent.py
	sed -i -e "s/ISOLATION_LEVEL_READ_UNCOMMITTED/$value/g" ./agent.py
	sed -i -e "s/ISOLATION_LEVEL_DEFAULT/$value/g" ./bad_agent.py
	sed -i -e "s/ISOLATION_LEVEL_AUTOCOMMIT/$value/g" ./bad_agent.py
	sed -i -e "s/ISOLATION_LEVEL_READ_COMMITTED/$value/g" ./bad_agent.py
	sed -i -e "s/ISOLATION_LEVEL_REPEATABLE_READ/$value/g" ./bad_agent.py
	sed -i -e "s/ISOLATION_LEVEL_SERIALIZABLE/$value/g" ./bad_agent.py
	sed -i -e "s/ISOLATION_LEVEL_READ_UNCOMMITTED/$value/g" ./bad_agent.py
	psql -f prepare_database.sql
	./run_elves.sh 
#	sleep 1
#	killall *.py
done
