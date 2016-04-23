#-------------------------------------------------------
#Author: Kahini
#This script creates keyspace and tables for db setup
#DBSchema: Tables are maintained candidate per se
#One General table for Tweets and 4 Tables for each analysis
#Table naming convention: candidateName_analysis
#-------------------------------------------------------

CREATE KEYSPACE IF NOT EXISTS TwitterDataSet WITH replication = {'class': 'SimpleStrategy',
'replication_factor': '1'} AND durable_writes = true;

USE TwitterDataSet;

#------------------------------------------------------------
#Tables for Donal Trump
#------------------------------------------------------------
CREATE TABLE IF NOT EXISTS realDonaldTrump_tweets (
counter bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at varchar,
sentiments_json varchar);

CREATE TABLE IF NOT EXISTS realDonaldTrump_sentencelevel (
counter bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at varchar,
sentiments_json varchar);

CREATE TABLE IF NOT EXISTS realDonaldTrump_wordcloud (
counter bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at varchar,
sentiments_json varchar);

CREATE TABLE IF NOT EXISTS realDonaldTrump_topics (
counter bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at varchar,
sentiments_json varchar);

CREATE TABLE IF NOT EXISTS realDonaldTrump_graph (
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

CREATE TABLE IF NOT EXISTS tedcruz (
counter bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at varchar,
sentiments_json varchar);

CREATE TABLE IF NOT EXISTS JohnKasich(
counter bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at varchar,
sentiments_json varchar);
