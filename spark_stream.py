from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def process_healthcare_data_stream():
    # Initialize the SparkSession
    spark = (
        SparkSession.builder
        .appName("HealthcareDataStreamProcessing")
        .config("spark.cassandra.connection.host", "cassandra")
        .config("spark.cassandra.connection.port", "9042")
        .config("es.nodes", "elasticsearch")
        .config("es.port", "9200")
        .getOrCreate()
    )

    # Set the checkpoint directory
    checkpoint_dir = "hdfs://namenode:9000/checkpoint/healthcare"

    # Read stream from Kafka topic
    healthcare_stream_df = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9093") \
        .option("subscribe", "healthcare_topic") \
        .option("startingOffsets", "earliest") \
        .load()
        # .option("kafka.consumer.fetch.max.wait.ms", "1000") \
        # .option("kafka.consumer.max.poll.interval.ms", "60000") \
       

    # Add Kafka ingestion timestamp as a new column
    healthcare_stream_df = healthcare_stream_df \
        .withColumn("event_time", col("timestamp").cast("timestamp"))

    # Kafka data contains the key and value as binary, so we need to convert it
    healthcare_data_df = healthcare_stream_df.selectExpr(
        "CAST(value AS STRING)",
        "event_time"
    ).selectExpr(
        "json_tuple(value, 'patient_id', 'age', 'gender', 'disease', 'treatment_cost', 'hospital_name') AS (patient_id, age, gender, disease, treatment_cost, hospital_name)",
        "event_time"
    )

    # Add a watermark and transform data: Group by disease and count occurrences
    transformed_data = healthcare_data_df \
        .withWatermark("event_time", "5 minutes") \
        .groupBy("disease") \
        .count()


    # Write transformed data to Elasticsearch
    elasticsearch_query = transformed_data.writeStream \
        .format("org.elasticsearch.spark.sql") \
        .option("checkpointLocation", checkpoint_dir + "/elasticsearch") \
        .outputMode("update") \
        .option("es.mapping.id", "patient_id") \
        .start("healthcare-disease-stats")

    # Write transformed data to Cassandra
    cassandra_query = transformed_data.writeStream \
        .format("org.apache.spark.sql.cassandra") \
        .option("checkpointLocation", checkpoint_dir + "/cassandra") \
        .outputMode("update") \
        .options(table="disease_stats", keyspace="healthcare") \
        .start()
    
    transformed_data.writeStream \
        .outputMode("complete") \
        .format("console") \
        .option("truncate", "false") \
        .start() \
        .awaitTermination()

    # Await termination of the streaming queries
    elasticsearch_query.awaitTermination()
    cassandra_query.awaitTermination()

    # Stop the Spark session when done
    spark.stop()

if __name__ == "__main__":
    process_healthcare_data_stream()
