use ARTSMUSEUM;

-- 1) Show all tables and explain how they are related to one another (keys, triggers, etc.)
select table_name, column_name, CONSTRAINT_NAME,REFERENCED_TABLE_NAME
from information_schema.key_column_usage, information_schema.triggers
where table_schema = 'ARTSMUSEUM';

select trigger_schema, trigger_name, action_statement
from information_schema.triggers
where TRIGGER_SCHEMA = 'ARTSMUSEUM';

-- 2) A basic retrieval query
select * from ART_OBJECT;

-- 3) A retrieval query with ordered results
select * from ARTIST
ORDER BY ARTIST_NAME ASC;

-- 4) A nested retrieval query
select* 
from created_by
where artist_name = "Pablo Picasso" and art_id_no in 
												(select paint_id_no
												 from painting)
											    OR
	artist_name = "Pablo Picasso" and art_id_no in 	 
												(select scul_id_no
												from sculpture);


-- 5) A retrieval query using joined tables
select O.Art_Description, S.SCUL_STYLE, S.SCUL_WEIGHT, S.SCUL_HEIGHT, S.SCUL_MATERIAL
from ART_OBJECT as O INNER JOIN SCULPTURE as S on O.ID_NO = S.SCUL_ID_NO;

-- 6) An update operation with any necessary triggers
DROP TRIGGER IF EXISTS duplicate_shown_pieces;
CREATE TRIGGER duplicate_shown_pieces
before update on SHOWN_DURING
for each ROW
set new.EXHIBITION_NAME = if ((select EXHIBITION_NAME from SHOWN_DURING where Art_ID_NO = new.Art_ID_NO) = new.EXHIBITION_NAME, 
new.EXHIBITION_NAME = 'UNKNOWN', 
new.EXHIBITION_NAME); -- Creation of trigger

UPDATE SHOWN_DURING SET Exhibition_Name = "Hear Me Now" WHERE Exhibition_Name = "Department of Recovery";

-- 7) A deletion operation with any necessary triggers

DELETE FROM CREATED_BY WHERE Artist_Name = "Adriaen van der Spelt" AND Art_Id_No = "002"; -- Constraint/trigger already added in ARTMUSEUM.sql file.

