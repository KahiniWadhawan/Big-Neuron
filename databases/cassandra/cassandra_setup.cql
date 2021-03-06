/* ---------------------------------------------------------------------
Author: Kahini Wadhawan
Contributor: Piyush Patel
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

/* ---------------------------------------------------------------------------------
Custom aggregate functions
Note: Cassandra has no default aggregate functions like group by or order by
----------------------------------------------------------------------------------- */
CREATE FUNCTION cusstate_group_and_total( state map<text, double>, type text, amount double )
CALLED ON NULL INPUT
RETURNS map<text, double>
LANGUAGE java AS '
Double count = (Double) state.get(type);  if (count == null) count = amount; else count = count + amount; state.put(type, count); return state; ' ;


CREATE OR REPLACE AGGREGATE cus_group_and_total(text, double)
SFUNC cusstate_group_and_total
STYPE map<text, double>
INITCOND {};


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
tweet_id varchar,
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
disgust_score double,
analytical_score double,
confident_score double,
tentative_score double,
openness_score double,
conscientiousness_score double,
extraversion_score double,
agreeableness_score double,
emotionalrange_score double,
PRIMARY KEY (tweet_id,date));
//revisit


/*------------------------------------------------------------
Table for Donald Trump Time to live tweets
------------------------------------------------------------*/
CREATE TABLE IF NOT EXISTS DonaldTrumpTTL (
tweet_id bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at timestamp
);

//revisit - decide on fields
CREATE TABLE IF NOT EXISTS realDonaldTrump_topics (
counter_val bigint primary key,
time_duration timestamp,  //could be maintained by week
topics_json text);

//revisit - decide on fields
CREATE TABLE IF NOT EXISTS realDonaldTrump_graph (
till_time timestamp primary key,
graph_json text);


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
tweet_id varchar,
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
disgust_score double,
analytical_score double,
confident_score double,
tentative_score double,
openness_score double,
conscientiousness_score double,
extraversion_score double,
agreeableness_score double,
emotionalrange_score double,
PRIMARY KEY (tweet_id,date));
//revisit


/*------------------------------------------------------------
Table for HillaryClinton Time to live tweets
------------------------------------------------------------*/
CREATE TABLE IF NOT EXISTS HillaryClintonTTL (
tweet_id bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at timestamp
);

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
tweet_id varchar,
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
disgust_score double,
analytical_score double,
confident_score double,
tentative_score double,
openness_score double,
conscientiousness_score double,
extraversion_score double,
agreeableness_score double,
emotionalrange_score double,
PRIMARY KEY (tweet_id,date));
//revisit


/*------------------------------------------------------------
Table for BernieSanders Time to live tweets
------------------------------------------------------------*/
CREATE TABLE IF NOT EXISTS BernieSandersTTL (
tweet_id bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at timestamp
);


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
tweet_id varchar,
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
disgust_score double,
analytical_score double,
confident_score double,
tentative_score double,
openness_score double,
conscientiousness_score double,
extraversion_score double,
agreeableness_score double,
emotionalrange_score double,
PRIMARY KEY (tweet_id,date));
//revisit


/*------------------------------------------------------------
Table for tedcruz Time to live tweets
------------------------------------------------------------*/
CREATE TABLE IF NOT EXISTS TedCruzTTL (
tweet_id bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at timestamp
);


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
tweet_id varchar,
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
disgust_score double,
analytical_score double,
confident_score double,
tentative_score double,
openness_score double,
conscientiousness_score double,
extraversion_score double,
agreeableness_score double,
emotionalrange_score double,
PRIMARY KEY (tweet_id,date));
//revisit


/*------------------------------------------------------------
Table for JohnKasich Time to live tweets
------------------------------------------------------------*/
CREATE TABLE IF NOT EXISTS JohnKasichTTL (
tweet_id bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at timestamp
);


//revisit - decide on fields
CREATE TABLE IF NOT EXISTS JohnKasich_topics (
counter_val bigint primary key,
time_duration timestamp,  //could be maintained by week
topics_json text);

//revisit - decide on fields
CREATE TABLE IF NOT EXISTS JohnKasich_graph (
till_time timestamp primary key,
graph_json text);


