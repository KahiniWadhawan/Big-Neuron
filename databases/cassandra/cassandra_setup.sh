#-------------------------------------------------------
#Author: Kahini | Piyush
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
tweet_id bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at timestamp);

#--------------------------------------------------------
#Sentence Level and Doc level analysis tables are merged
#-------------------------------------------------------

CREATE TABLE IF NOT EXISTS realDonaldTrump_sentencelevel (
tweet_id bigint primary key,
created_at timestamp,
tone_json text,
emotion_json text,
writing_json text,
social_json text,
anger_score double,
joy_score double,
fear_score double,
sadness_score double,
disgust_score double);

#CREATE TABLE IF NOT EXISTS realDonaldTrump_wordcloud (
#counter bigint primary key,
#tweet_text varchar,
#lang varchar,
#retweet_count bigint);

#revisit - decide on fields
CREATE TABLE IF NOT EXISTS realDonaldTrump_topics (
time_duration primary key,  #could be maintained by week
topics_json text);

#revisit - decide on fields
CREATE TABLE IF NOT EXISTS realDonaldTrump_graph (
till_time timestamp primary key,
graph_json text);





#------------------------------------------------------------
#Tables for Donald Trump Time to live tweets
#------------------------------------------------------------
CREATE TABLE IF NOT EXISTS DonaldTrumpTTL (
tweet_id bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at timestamp,
deviceused varchar,
possibly_sensitive varchar,
coordinates varchar,
fav_cout varchar,
geo varchar,
place varchar
);








#------------------------------------------------------
#Tables for HillaryClinton
#------------------------------------------------------
CREATE TABLE IF NOT EXISTS HillaryClinton_tweets (
tweet_id bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at timestamp);

#--------------------------------------------------------
#Sentence Level and Doc level analysis tables are merged
#-------------------------------------------------------

CREATE TABLE IF NOT EXISTS HillaryClinton_sentencelevel (
tweet_id bigint primary key,
created_at timestamp,
tone_json text,
emotion_json text,
writing_json text,
social_json text,
anger_score double,
joy_score double,
fear_score double,
sadness_score double,
disgust_score double);

#CREATE TABLE IF NOT EXISTS HillaryClinton_wordcloud (
#counter bigint primary key,
#tweet_text varchar,
#lang varchar,
#retweet_count bigint);

#revisit - decide on fields
CREATE TABLE IF NOT EXISTS HillaryClinton_topics (
time_duration primary key,  #could be maintained by week
topics_json text);

#revisit - decide on fields
CREATE TABLE IF NOT EXISTS HillaryClinton_graph (
till_time timestamp primary key,
graph_json text);



#------------------------------------------------------------
#Tables for HillaryClinton Time to live tweets
#------------------------------------------------------------
CREATE TABLE IF NOT EXISTS HillaryClintonTTL (
tweet_id bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at timestamp,
deviceused varchar,
possibly_sensitive varchar,
coordinates varchar,
fav_cout varchar,
geo varchar,
place varchar
);






#------------------------------------------------------
#Tables for BernieSanders
#------------------------------------------------------

CREATE TABLE IF NOT EXISTS BernieSanders_tweets (
tweet_id bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at timestamp);

#--------------------------------------------------------
#Sentence Level and Doc level analysis tables are merged
#-------------------------------------------------------

CREATE TABLE IF NOT EXISTS BernieSanders_sentencelevel (
tweet_id bigint primary key,
created_at timestamp,
tone_json text,
emotion_json text,
writing_json text,
social_json text,
anger_score double,
joy_score double,
fear_score double,
sadness_score double,
disgust_score double);

#CREATE TABLE IF NOT EXISTS BernieSanders_wordcloud (
#counter bigint primary key,
#tweet_text varchar,
#lang varchar,
#retweet_count bigint);

#revisit - decide on fields
CREATE TABLE IF NOT EXISTS BernieSanders_topics (
time_duration primary key,  #could be maintained by week
topics_json text);

#revisit - decide on fields
CREATE TABLE IF NOT EXISTS BernieSanders_graph (
till_time timestamp primary key,
graph_json text);


#------------------------------------------------------------
#Tables for BernieSanders Time to live tweets
#------------------------------------------------------------
CREATE TABLE IF NOT EXISTS BernieSandersTTL (
tweet_id bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at timestamp,
deviceused varchar,
possibly_sensitive varchar,
coordinates varchar,
fav_cout varchar,
geo varchar,
place varchar
);






#------------------------------------------------------
#Tables for tedcruz
#------------------------------------------------------

CREATE TABLE IF NOT EXISTS tedcruz_tweets (
tweet_id bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at timestamp);

#--------------------------------------------------------
#Sentence Level and Doc level analysis tables are merged
#-------------------------------------------------------

CREATE TABLE IF NOT EXISTS tedcruz_sentencelevel (
tweet_id bigint primary key,
created_at timestamp,
tone_json text,
emotion_json text,
writing_json text,
social_json text,
anger_score double,
joy_score double,
fear_score double,
sadness_score double,
disgust_score double);

#CREATE TABLE IF NOT EXISTS tedcruz_wordcloud (
#counter bigint primary key,
#tweet_text varchar,
#lang varchar,
#retweet_count bigint);

#revisit - decide on fields
CREATE TABLE IF NOT EXISTS tedcruz_topics (
time_duration primary key,  #could be maintained by week
topics_json text);

#revisit - decide on fields
CREATE TABLE IF NOT EXISTS tedcruz_graph (
till_time timestamp primary key,
graph_json text);





#------------------------------------------------------------
#Tables for tedcruz Time to live tweets
#------------------------------------------------------------
CREATE TABLE IF NOT EXISTS TedCruzTTL (
tweet_id bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at timestamp,
deviceused varchar,
possibly_sensitive varchar,
coordinates varchar,
fav_cout varchar,
geo varchar,
place varchar
);




#------------------------------------------------------
#Tables for JohnKasich
#------------------------------------------------------

CREATE TABLE IF NOT EXISTS JohnKasich_tweets (
tweet_id bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at timestamp);

#--------------------------------------------------------
#Sentence Level and Doc level analysis tables are merged
#-------------------------------------------------------

CREATE TABLE IF NOT EXISTS JohnKasich_sentencelevel (
tweet_id bigint primary key,
created_at timestamp,
tone_json text,
emotion_json text,
writing_json text,
social_json text,
anger_score double,
joy_score double,
fear_score double,
sadness_score double,
disgust_score double);

#CREATE TABLE IF NOT EXISTS JohnKasich_wordcloud (
#counter bigint primary key,
#tweet_text varchar,
#lang varchar,
#retweet_count bigint);

#revisit - decide on fields
CREATE TABLE IF NOT EXISTS JohnKasich_topics (
time_duration primary key,  #could be maintained by week
topics_json text);

#revisit - decide on fields
CREATE TABLE IF NOT EXISTS JohnKasich_graph (
till_time timestamp primary key,
graph_json text);


#------------------------------------------------------------
#Tables for JohnKasich Time to live tweets
#------------------------------------------------------------
CREATE TABLE IF NOT EXISTS JohnKasichTTL (
tweet_id bigint primary key,
tweet_text varchar,
lang varchar,
retweet_count bigint,
created_at timestamp,
deviceused varchar,
possibly_sensitive varchar,
coordinates varchar,
fav_cout varchar,
geo varchar,
place varchar
);



