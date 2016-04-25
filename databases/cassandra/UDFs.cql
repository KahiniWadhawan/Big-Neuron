/* 
Author: Kahini Wadhawan
This file has custom aggregate functions
Note: Cassandra has no default aggregate functions like group by or order by
*/

USE TwitterDataSet;


CREATE FUNCTION cusstate_group_and_total( state map<text, double>, type text, amount double )
CALLED ON NULL INPUT
RETURNS map<text, double>
LANGUAGE java AS '
Double count = (Double) state.get(type);  if (count == null) count = amount; else count = count + amount; state.put(type, count); return state; ' ;


CREATE OR REPLACE AGGREGATE cus_group_and_total(text, double) 
SFUNC cusstate_group_and_total 
STYPE map<text, double> 
INITCOND {};
