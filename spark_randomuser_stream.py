import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, concat_ws
from pyspark.sql.types import StructType, StringType, IntegerType
import requests

# API'ye gönderimi yapan fonksiyon
def send_to_api(df, epoch_id):
    for row in df.collect():
        payload = {
            "first_name": row['first_name'],
            "last_name": row['last_name'],
            "fullname": row['fullname'],
            "email": row['email'],
            "gender": row['gender'],
            "country": row['country'],
            "age": row['age']
        }
        try:
            requests.post("http://localhost:5000/add_user", json=payload)
        except Exception as e:
            print("Spark→API hata:", e)

# SparkSession başlat
spark = SparkSession.builder \
    .appName("RandomUserToAPI") \
    .master("local[*]") \
    .getOrCreate()

# JSON şeması: name, email, gender, dob, location
schema = StructType() \
    .add("name", StructType()
         .add("first", StringType())
         .add("last", StringType())) \
    .add("email", StringType()) \
    .add("gender", StringType()) \
    .add("dob", StructType().add("age", IntegerType())) \
    .add("location", StructType().add("country", StringType()))

# Kafka'dan veri oku
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "user-topic") \
    .option("startingOffsets", "latest") \
    .load()

# JSON'u ayıkla ve gerekli kolonları çıkar
json_df = df.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json(col("json_str"), schema).alias("data")) \
    .select(
        col("data.name.first").alias("first_name"),
        col("data.name.last").alias("last_name"),
        concat_ws(" ", col("data.name.first"), col("data.name.last")).alias("fullname"),
        col("data.email").alias("email"),
        col("data.gender").alias("gender"),
        col("data.location.country").alias("country"),
        col("data.dob.age").alias("age")
    )

# Streaming query: her batch'te API'ye gönder
query = json_df.writeStream \
    .foreachBatch(send_to_api) \
    .outputMode("append") \
    .start()

query.awaitTermination()
