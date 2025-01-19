**Real-World Hands-On Big Data Analytics with Docker Compose**

This repository demonstrates a real-world big data analytics workflow using Docker Compose with Hadoop, Spark, Kafka, Elasticsearch, Flink, Presto, and Cassandra. The use case focuses on analyzing healthcare data.

**Prerequisites**

- Docker and Docker Compose installed.
- Minimum 8 GB RAM and sufficient disk space.

**Getting Started**

**Clone the Repository**

git clone https://github.com/silwalprabin/big-data-workshop-iims

cd bigdata-analytics

**Services Overview**

- **Hadoop (HDFS)**: Distributed storage for big data.
- **Spark**: Distributed data processing and analytics engine.
- **Kafka**: Distributed streaming platform.
- **Elasticsearch**: Search and analytics engine.
- **Kibana**: Visualization tool for Elasticsearch.
- **Flink**: Real-time stream processing.
- **Presto**: SQL query engine for large datasets.
- **Cassandra**: NoSQL database for scalable storage.

**Setup Environment Variables**

See hadoop.env file

**Start the Cluster**

Run the following command to start all services:
```
docker-compose up -d
```

Verify that all services are running:
```
docker-compose ps
```


**Accessing Services**

- **Hadoop Namenode UI**: [http://localhost:9870](http://localhost:9870/)
- **Spark Master UI**: [http://localhost:8080](http://localhost:8080/)
- **Kafka**: <localhost:9092>
- **Elasticsearch**: [http://localhost:9200](http://localhost:9200/)
- **Kibana**: [http://localhost:5601](http://localhost:5601/)
- **Flink**: [http://localhost:8082](http://localhost:8082/)
- **Presto**: [http://localhost:8083](http://localhost:8083/)
- **Cassandra**: <localhost:9042>

**Verify realtime events**
```
docker exec -it kafka /bin/bash

kafka-topics.sh --create --topic healthcare_topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic healthcare_topic

exit
```

**Stop realtime events**
```
docker stop kafka-producer
```

**Use Case: Healthcare Data Analysis**

The workflow involves ingesting healthcare data into Kafka, processing it with Spark, querying processed data with Presto, and storing results in Cassandra and Elasticsearch for visualization with Kibana.

**Data Preparation**

[Sample healthcare_data.csv]
Dataset (healthcare_data.csv) includes the following columns:
- patient_id: Unique identifier for the patient.
- age: Age of the patient.
- gender: Gender of the patient.
- disease: Diagnosed disease.
- treatment_cost: Cost of treatment.
- hospital_name: Name of the hospital.

**Kafka Producer Container: Data Streaming**

See kafka-producer/kafka_producer.py file will generate healthcare_data with above sample

**Spark Script: Batch Processing**

See spark_job.py

**Spark Script: Stream Processing**

See spark_stream.py


**Cassandra:**

Cassandra stores healthcare data (e.g., patient records, lab results).


**Steps to Run Spark Job**

1. Copy the data to HDFS:

```Docker
docker cp healthcare_data.csv namenode:/

docker exec -it namenode bash

hadoop fs -mkdir -p /data

hadoop fs -put /healthcare_data.csv /data

exit
```

2. Submit the Spark job:

```
docker cp spark_job.py spark-master:/

docker cp spark_stream.py spark-master:/

docker exec -it cassandra cqlsh

CREATE KEYSPACE healthcare WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE healthcare;

CREATE TABLE disease_stats (
    disease text PRIMARY KEY,
    count int
);

exit
```

```
docker exec -it spark-master bash

pip3 install cassandra-driver

TEST:: (/spark/bin/spark-class org.apache.spark.deploy.worker.Worker spark://spark-master:7077)


/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  --conf spark.cassandra.connection.host=cassandra \
  --conf spark.cassandra.connection.port=9042 \
  --packages org.apache.spark:spark-sql_2.12:3.4.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.0,org.elasticsearch:elasticsearch-spark-30_2.12:8.10.2,com.github.jnr:jnr-posix:3.1.15 \
  spark_job.py

exit
```

# Verify Data in Cassandra
```
docker exec -it cassandra cqlsh

USE healthcare;

SELECT * FROM disease_stats;

exit
```

# Verify Data in Elasticsearch
```
curl -X GET "http://localhost:9200/healthcare-disease-stats/_search?pretty"
```

RUN:

**Start realtime events**
```
docker start kafka-producer
```
**Verify realtime events**
```
docker exec -it kafka /bin/bash

kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic healthcare_topic --from-beginning

exit
```

```
docker exec -it spark-master bash

/spark/bin/spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql_2.12:3.4.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.0,org.elasticsearch:elasticsearch-spark-30_2.12:8.10.2,com.github.jnr:jnr-posix:3.1.15,org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 /spark_stream.py

exit
```

**Data Visualization with Kibana**

1. Open Kibana at [http://localhost:5601](http://localhost:5601/).
2. Open http://localhost:5601/app/discover
    Configure an index pattern for healthcare*.
3. Create visualizations and dashboards.


**Troubleshooting**

- Check logs for any service:

- docker-compose logs <container_name>

- Verify resource allocation for Docker.


**Stream Processing with Flink**

See iot-stream-flink.py file:



**Query Processed Data with Presto:**

Use case id to access the Presto UI at http://localhost:8083 and run SQL queries like:

Eg: SELECT disease, count FROM healthcare.disease_stats;

We can configure Presto to connect with:

- Cassandra: To query structured data.

- HDFS: For querying large-scale, distributed data.

- Elasticsearch: To query indexed healthcare data.


**Conclusion**

This setup allows hands-on exploration of big data technologies using a healthcare data analytics use case. Customize the scripts and workflows to explore advanced scenarios.

