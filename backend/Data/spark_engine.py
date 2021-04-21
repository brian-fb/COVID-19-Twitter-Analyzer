from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F
import shutil
import os
#os.environ['SPARK_HOME'] = '/Users/mgeek/opt/anaconda3/envs/twitter/lib/python3.7/site-packages/pyspark/'

def preprocessing(lines):
    words = lines.select(explode(split(lines.value, "t_end")).alias("word"))
    words = words.na.replace('', None)
    words = words.na.drop()

    return words

def spark_engine():
    # create Spark session

    if os.path.exists('./result/spark_cache/parc'):
        shutil.rmtree('./result/spark_cache/parc')
    if os.path.exists('./result/spark_cache/check'):
        shutil.rmtree('./result/spark_cache/check')

    spark = SparkSession.builder.appName("TwitterSentimentAnalysis").getOrCreate()

    # read the tweet data from socket
    lines = spark.readStream.format("socket").option("host", "0.0.0.0").option("port", 5555).load()
    # Preprocess the data
    words = preprocessing(lines)
    words = words.repartition(1)
    query = words.writeStream.queryName("all_tweets") \
        .outputMode("append").format("parquet") \
        .option("path", "./result/spark_cache/parc") \
        .option("checkpointLocation", "./result/spark_cache/check") \
        .trigger(processingTime='30 seconds').start()
    query.awaitTermination()

if __name__ == "__main__":
    # create Spark session

    spark_engine()
    # if os.path.exists('./result/spark_cache/parc'):
    #     shutil.rmtree('./result/spark_cache/parc')
    # if os.path.exists('./result/spark_cache/check'):
    #     shutil.rmtree('./result/spark_cache/check')
    #
    # spark = SparkSession.builder.appName("TwitterSentimentAnalysis").getOrCreate()
    #
    # # read the tweet data from socket
    # lines = spark.readStream.format("socket").option("host", "0.0.0.0").option("port", 5555).load()
    # # Preprocess the data
    # words = preprocessing(lines)
    # words = words.repartition(1)
    # query = words.writeStream.queryName("all_tweets")\
    #     .outputMode("append").format("parquet")\
    #     .option("path", "./result/spark_cache/parc")\
    #     .option("checkpointLocation", "./result/spark_cache/check")\
    #     .trigger(processingTime='60 seconds').start()
    # query.awaitTermination()