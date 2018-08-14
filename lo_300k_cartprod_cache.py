import time
import random
import pyspark.sql.functions as func
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql import HiveContext, SQLContext
import math
from pyspark.mllib.random  import RandomRDDs 
from pyspark.sql.types import *
#from pyspark.sql.functions import *
from pyspark.sql.types import Row
spark = SparkSession.builder.config("spark.sql.crossJoin.enabled","true").getOrCreate() 

n=300000

# create rdd of random floats
nRow = n
nCol = 4
seed = 5
numPartitions=32

rdd1 = RandomRDDs.normalVectorRDD(spark, nRow, nCol,numPartitions,seed) 
seed = 3
rdd2 = RandomRDDs.normalVectorRDD(spark, nRow, nCol,numPartitions,seed) 
sc = spark.sparkContext

# convert each tuple in the rdd to a row
randomNumberRdd1 = rdd1.map(lambda x: Row(A=float(x[0]), B=float(x[1]), C=float(x[2]), D=float(x[3]))) 
randomNumberRdd2 = rdd2.map(lambda x: Row(E=float(x[0]), F=float(x[1]), G=float(x[2]), H=float(x[3])))

# create dataframe from rdd
schemaRandomNumberDF1 = spark.createDataFrame(randomNumberRdd1)
schemaRandomNumberDF2 = spark.createDataFrame(randomNumberRdd2)

# cache the dataframe
schemaRandomNumberDF1.cache()

cross_df = schemaRandomNumberDF1.crossJoin(schemaRandomNumberDF2)

# aggregate 
results = schemaRandomNumberDF1.groupBy("A").agg(func.max("B"),func.sum("C"))
results.show(n=100)
print "----------Count in cross-join--------------- {0}".format(cross_df.count()) 
