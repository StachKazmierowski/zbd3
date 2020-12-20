DROP FOREIGN TABLE slodycz_w_magazynie_csv;
CREATE FOREIGN TABLE slodycz_w_magazynie_csv (
	nazwa varchar,
	ilosc_pozostalych integer
) server csv
OPTIONS( filename '/home/stach/ZBD/zbd3/data/sweets.csv', format 'csv');
DROP TABLE slodycz_w_magazynie;
CREATE TABLE slodycz_w_magazynie AS select * from slodycz_w_magazynie_csv;
ALTER TABLE slodycz_w_magazynie ADD CONSTRAINT sprawdz_liczbe_slodyczy
	CHECK ( ilosc_pozostalych >= 0);

DROP FOREIGN TABLE podobny_slodycz_csv;
CREATE FOREIGN TABLE podobny_slodycz_csv (
	ktory_slodycz_jest_podobny varchar,
	do_czego_slodycz_jest_podobny varchar,
	podobienstwo real
) server csv
OPTIONS( filename '/home/stach/ZBD/zbd3/data/similarity.csv', format 'csv');
DROP TABLE podobny_slodycz;
CREATE TABLE podobny_slodycz AS select * from podobny_slodycz_csv;

DROP TABLE paczka;
CREATE TABLE paczka (
	id SERIAL PRIMARY KEY,
	kraj varchar,
	opis_obdarowanego varchar
);

DROP TABLE slodycz_w_paczce;
CREATE TABLE slodycz_w_paczce (
	id_paczki integer,
	slodycz varchar,
	ilosc integer
);



DROP FOREIGN TABLE paczka_pomocnicza_csv;
CREATE FOREIGN TABLE paczka_pomocnicza_csv (
	id integer,
	kraj varchar,
	opis_obdarowanego varchar,
	slodycz varchar,
	ilosc integer
) server csv
OPTIONS( filename '/home/stach/ZBD/zbd3/data/paczki.csv', format 'csv');
DROP TABLE paczka_pomocnicza;
CREATE TABLE paczka_pomocnicza AS select * from paczka_pomocnicza_csv;