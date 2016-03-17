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
