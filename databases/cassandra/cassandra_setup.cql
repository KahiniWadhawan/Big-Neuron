/* ---------------------------------------------------------------------
Author: Kahini
This script creates keyspace and tables for db setup
DBSchema: Tables are maintained candidate per se
One General table for Tweets and 4 Tables for each analysis
Table naming convention: candidateName_analysis
Usage: run this command in cqlsh: SOURCE 'path-to-/cassandra_setup.cql'
-------------------------------------------------------------------------
*/

CREATE KEYSPACE IF NOT EXISTS TwitterDataSet WITH replication = {'class': 'SimpleStrategy',
'replication_factor': '1'} AND durable_writes = true;

USE TwitterDataSet;

/* ------------------------------------------------------------
Tables for Donald Trump
------------------------------------------------------------ */
CREATE TABLE IF NOT EXISTS realDonaldTrump_tweets (
tweet_id varchar primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at varchar,
date varchar,
time varchar
/*day varchar,
month varchar,
year varchar,
time varchar*/);

/* --------------------------------------------------------
Sentence Level and Doc level analysis tables are merged
---------------------------------------------------------- */

CREATE TABLE IF NOT EXISTS realDonaldTrump_sentencelevel (
tweet_id varchar primary key,
created_at varchar,
date varchar,
time varchar,
tone_json text,
emotion_json text,
writing_json text,
social_json text,
anger_score double,
joy_score double,
fear_score double,
sadness_score double,
disgust_score double);

/*
CREATE TABLE IF NOT EXISTS realDonaldTrump_wordcloud (
counter bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint);
*/

//revisit - decide on fields
CREATE TABLE IF NOT EXISTS realDonaldTrump_topics (
counter_val bigint primary key,
time_duration timestamp,  //could be maintained by week
topics_json text);

//revisit - decide on fields
CREATE TABLE IF NOT EXISTS realDonaldTrump_graph (
till_time timestamp primary key,
graph_json text);

/*
/* ------------------------------------------------------
Tables for HillaryClinton
--------------------------------------------------------- */
CREATE TABLE IF NOT EXISTS HillaryClinton_tweets (
tweet_id varchar primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at varchar,
date varchar,
time varchar
/*day varchar,
month varchar,
year varchar,
time varchar*/);

/* --------------------------------------------------------
Sentence Level and Doc level analysis tables are merged
---------------------------------------------------------- */

CREATE TABLE IF NOT EXISTS HillaryClinton_sentencelevel (
tweet_id varchar primary key,
created_at varchar,
date varchar,
time varchar,
tone_json text,
emotion_json text,
writing_json text,
social_json text,
anger_score double,
joy_score double,
fear_score double,
sadness_score double,
disgust_score double);

/*
CREATE TABLE IF NOT EXISTS HillaryClinton_wordcloud (
counter bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint);
*/

//revisit - decide on fields
CREATE TABLE IF NOT EXISTS HillaryClinton_topics (
counter_val bigint primary key,
time_duration timestamp,  //could be maintained by week
topics_json text);

//revisit - decide on fields
CREATE TABLE IF NOT EXISTS HillaryClinton_graph (
till_time timestamp primary key,
graph_json text);


/* ------------------------------------------------------
Tables for BernieSanders
--------------------------------------------------------- */
CREATE TABLE IF NOT EXISTS BernieSanders_tweets (
tweet_id varchar primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at varchar,
date varchar,
time varchar
/*day varchar,
month varchar,
year varchar,
time varchar*/);

/* --------------------------------------------------------
Sentence Level and Doc level analysis tables are merged
---------------------------------------------------------- */

CREATE TABLE IF NOT EXISTS BernieSanders_sentencelevel (
tweet_id varchar primary key,
created_at varchar,
date varchar,
time varchar,
tone_json text,
emotion_json text,
writing_json text,
social_json text,
anger_score double,
joy_score double,
fear_score double,
sadness_score double,
disgust_score double);

/*
CREATE TABLE IF NOT EXISTS BernieSanders_wordcloud (
counter bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint);
*/

//revisit - decide on fields
CREATE TABLE IF NOT EXISTS BernieSanders_topics (
counter_val bigint primary key,
time_duration timestamp,  //could be maintained by week
topics_json text);

//revisit - decide on fields
CREATE TABLE IF NOT EXISTS BernieSanders_graph (
till_time timestamp primary key,
graph_json text);


/* ------------------------------------------------------
Tables for tedcruz
-------------------------------------------------------- */
CREATE TABLE IF NOT EXISTS tedcruz_tweets (
tweet_id varchar primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at varchar,
date varchar,
time varchar
/*day varchar,
month varchar,
year varchar,
time varchar*/);

/* --------------------------------------------------------
Sentence Level and Doc level analysis tables are merged
---------------------------------------------------------- */

CREATE TABLE IF NOT EXISTS tedcruz_sentencelevel (
tweet_id varchar primary key,
created_at varchar,
date varchar,
time varchar,
tone_json text,
emotion_json text,
writing_json text,
social_json text,
anger_score double,
joy_score double,
fear_score double,
sadness_score double,
disgust_score double);

/*
CREATE TABLE IF NOT EXISTS tedcruz_wordcloud (
counter bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint);
*/

//revisit - decide on fields
CREATE TABLE IF NOT EXISTS tedcruz_topics (
counter_val bigint primary key,
time_duration timestamp,  //could be maintained by week
topics_json text);

//revisit - decide on fields
CREATE TABLE IF NOT EXISTS tedcruz_graph (
till_time timestamp primary key,
graph_json text);


/* ------------------------------------------------------
Tables for JohnKasich
--------------------------------------------------------- */
CREATE TABLE IF NOT EXISTS JohnKasich_tweets (
tweet_id varchar primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at varchar,
date varchar,
time varchar
/*day varchar,
month varchar,
year varchar,
time varchar*/);

/* --------------------------------------------------------
Sentence Level and Doc level analysis tables are merged
---------------------------------------------------------- */

CREATE TABLE IF NOT EXISTS JohnKasich_sentencelevel (
tweet_id varchar primary key,
created_at varchar,
date varchar,
time varchar,
tone_json text,
emotion_json text,
writing_json text,
social_json text,
anger_score double,
joy_score double,
fear_score double,
sadness_score double,
disgust_score double);

/*
CREATE TABLE IF NOT EXISTS JohnKasich_wordcloud (
counter bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint);
*/

//revisit - decide on fields
CREATE TABLE IF NOT EXISTS JohnKasich_topics (
counter_val bigint primary key,
time_duration timestamp,  //could be maintained by week
topics_json text);

//revisit - decide on fields
CREATE TABLE IF NOT EXISTS JohnKasich_graph (
till_time timestamp primary key,
graph_json text);


*/