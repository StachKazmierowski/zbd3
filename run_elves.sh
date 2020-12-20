#!/bin/bash
psql -f prepare_database.sql
python time_tracker.py &
for i in {1,..,10}
do
	python agent.py &
	python bad_agent.py &
done

