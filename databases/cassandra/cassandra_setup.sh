#-------------------------------------------------------
#Author: Kahini
#This script creates keyspace and tables for db setup
#-------------------------------------------------------
CREATE KEYSPACE IF NOT EXISTS TwitterDataSet WITH replication = {'class': 'SimpleStrategy',
'replication_factor': '1'} AND durable_writes = true;

USE TwitterDataSet;

CREATE TABLE IF NOT EXISTS realDonaldTrump (
counter bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at varchar,
sentiments_json varchar);

CREATE TABLE IF NOT EXISTS HillaryClinton (
counter bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at varchar,
sentiments_json varchar);

CREATE TABLE IF NOT EXISTS BernieSanders (
counter bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at varchar,
sentiments_json varchar);
