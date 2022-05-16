# ETL Pipeline for Sparkify 

## About the project

<p>This project simplifies querying of the songs and user activity data for better analysis of user behaviour.</p>

<p> Currently the data is stored in two directories containaing JSON files with Song and Log dataset, which is not ideal for querying.</p>

<p>Through this ETL pipeline we ingest data into a postgres database with star schema that focuses on analysis based on user activity (i.e.dataset that answers the analytical question "which songs users are listening to").</p>

## Built with

- Python
- Pandas
- psycopg2
- Postgres
- SQL

## Getting started

In order to run ETL pipeline, run the following commands in your terminal:

- `python create_tables.py`: this file creates tables in postgres if not present or drops and recreates them if tables are already present

- `python etl.py`: this file performs the ETL of data

- `test.ipynb notebook`: run this file to test if data got ingested in the database 

## Scripts

- **sql_queries.py** - contains queries that perform select and insert records as well as drop table queries

- **create_tables.py** - connects to the database and creates tables in database using queries present in sql_queries.py

- **etl.py** - this file processes both the log and song dataset then performs ETL and loads the whole dataset into the database 

- **test.ipynb** - you can use this notebook to check the inserted records and check if the tables conform to certain constraints

## Database design

This project leverages use of Star schema design.

> will add 

State and justify your database schema design and ETL pipeline.



