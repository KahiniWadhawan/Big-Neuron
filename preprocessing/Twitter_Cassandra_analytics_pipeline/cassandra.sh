'''
============================================================================
Name        : Cassandra Script
Author      : Piyush
Version     : 1
Copyright   : DS
Description : 
Script for cassandra :
This is the current Keyspace the table is created on and the column name the table consists.

Since all of these wil;l go inse the code, this is temporary, but it will give you an intution of 
what the current schema is in the DB.
============================================================================
'''

CREATE KEYSPACE TwitterDataSet
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };


USE TwitterDataSet;


CREATE TABLE Tweepy (
counter bigint,
tweet varchar,
lang varchar,
sourcee varchar,
retweet_count bigint,
created_at varchar,
analytics varchar,
PRIMARY KEY (counter));
