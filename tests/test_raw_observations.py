import os
from pyspark.sql import SparkSession
import pytest

@pytest.fixture()
def spark():
    spark = SparkSession.builder \
            .master("local") \
            .config("spark.jars","/home/boon/temp/postgresql-42.7.7.jar") \
            .getOrCreate()
    return spark

@pytest.fixture()
def df(spark):
    df = spark.read \
        .format("jdbc") \
        .option("url",f"jdbc:postgresql://{os.environ['POSTGRES_HOST']}:5433/{os.environ['POSTGRES_DB']}") \
        .option("dbtable","public_raw.raw_obs") \
        .option("user",f"{os.environ['POSTGRES_USER']}") \
        .option("password",f"{os.environ['POSTGRES_PASS']}") \
        .option("driver","org.postgresql.Driver") \
        .load()

    df.createOrReplaceTempView("observations")

    return df

# tests:
    # Distinct taxonKey, scientific_name pairs
    #
def test_ranks(df):
    return
