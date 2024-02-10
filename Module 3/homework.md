## Week 3 Homework

<b>SETUP:</b></br>
Create an external table using the Green Taxi Trip Records Data for 2022. </br>
Create a table in BQ using the Green Taxi Trip Records for 2022 (do not partition or cluster this table). </br>
</p>

Creating external table
```
CREATE OR REPLACE EXTERNAL TABLE `nyc_taxi_trips.green-taxi-data-external`
OPTIONS (
  format = 'parquet',
  uris = ['gs://bucket-name/file-name']
);
```

Creating the internal table
```
CREATE TABLE `nyc_taxi_trips.green-taxi-data` AS (
  SELECT DATE(TIMESTAMP_MICROS(CAST(lpep_pickup_datetime / 1000 AS INT64))) as lpep_pickup_date,  * FROM `nyc_taxi_trips.green-taxi-data-external`
);
```

## Question 1:
Question 1: What is count of records for the 2022 Green Taxi Data??
- 65,623,481
- 840,402
- 1,936,423
- 253,647

<br/>

>Answer

```
840,402
```

>SQL Query

```
SELECT COUNT(1) FROM `nyc_taxi_trips.green-taxi-data`;
```

<br/>

## Question 2:
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.</br> 
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

- 0 MB for the External Table and 6.41MB for the Materialized Table
- 18.82 MB for the External Table and 47.60 MB for the Materialized Table
- 0 MB for the External Table and 0MB for the Materialized Table
- 2.14 MB for the External Table and 0MB for the Materialized Table

<br/>

>Answer

```
0 MB for the External Table and 6.41MB for the Materialized Table
```

>SQL Query
```
SELECT COUNT(DISTINCT(PULocationID)) FROM `nyc_taxi_trips.green-taxi-data-external`;

SELECT COUNT(DISTINCT(PULocationID)) FROM `nyc_taxi_trips.green-taxi-data`;
```

<br/>

## Question 3:
How many records have a fare_amount of 0?
- 12,488
- 128,219
- 112
- 1,622

<br/>

>Answer

```
1,622
```

>SQL Query
```
SELECT COUNT(*) FROM `nyc_taxi_trips.green-taxi-data-external` WHERE  fare_amount=0;
```

<br/>

## Question 4:
What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime? (Create a new table with this strategy)
- Cluster on lpep_pickup_datetime Partition by PUlocationID
- Partition by lpep_pickup_datetime  Cluster on PUlocationID
- Partition by lpep_pickup_datetime and Partition by PUlocationID
- Cluster on by lpep_pickup_datetime and Cluster on PUlocationID

<br/>

>Answer

```
Partition by lpep_pickup_datetime  Cluster on PUlocationID
```

>SQL Query
```
CREATE OR REPLACE TABLE `nyc_taxi_trips.green-taxi-data-partitioned`
PARTITION BY lpep_pickup_date
CLUSTER BY PULocationID AS (
  SELECT * FROM `nyc_taxi_trips.green-taxi-data`
);
```

<br/>

## Question 5:
Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime
06/01/2022 and 06/30/2022 (inclusive)</br>

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values? </br>

Choose the answer which most closely matches.</br> 

- 22.82 MB for non-partitioned table and 647.87 MB for the partitioned table
- 12.82 MB for non-partitioned table and 1.12 MB for the partitioned table
- 5.63 MB for non-partitioned table and 0 MB for the partitioned table
- 10.31 MB for non-partitioned table and 10.31 MB for the partitioned table

<br/>

>Answer

```
12.82 MB for non-partitioned table and 1.12 MB for the partitioned table
```

>SQL Query

```
SELECT COUNT(DISTINCT(PULocationID)) FROM `nyc_taxi_trips.green-taxi-data` WHERE lpep_pickup_date BETWEEN '2022-06-01' AND '2022-06-30';

SELECT COUNT(DISTINCT(PULocationID)) FROM `nyc_taxi_trips.green-taxi-data-partitioned` WHERE lpep_pickup_date BETWEEN '2022-06-01' AND '2022-06-30';
```

<br/>

## Question 6: 
Where is the data stored in the External Table you created?

- Big Query
- GCP Bucket
- Big Table
- Container Registry

<br/>

>Answer

```
GCP Bucket
```

<br/>

## Question 7:
It is best practice in Big Query to always cluster your data:
- True
- False

<br/>

>Answer

```
False
```