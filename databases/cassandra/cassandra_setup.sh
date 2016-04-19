#-------------------------------------------------------
#Author: Kahini
#This script creates keyspace and tables for db setup
#-------------------------------------------------------
CREATE KEYSPACE IF NOT EXISTS TwitterDataSet WITH replication = {'class': 'SimpleStrategy',
'replication_factor': '1'} AND durable_writes = true;

USE TwitterDataSet;