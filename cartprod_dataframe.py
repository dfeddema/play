import time
import random
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql import HiveContext, SQLContext
import math
from pyspark.mllib.random  import RandomRDDs 
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.types import Row
spark = SparkSession.builder.config("spark.sql.crossJoin.enabled","true").getOrCreate() 

n=500000

# create RDD of random floats
nRow = n
nCol = 4
seed = 5
numPartitions=32
rdd = RandomRDDs.normalVectorRDD(spark, nRow, nCol,numPartitions,seed) 
sc = spark.sparkContext
print "number of partitions in RDD"
print rdd.getNumPartitions()

# convert each tuple in the rdd to a row
randomNumberRdd = rdd.map(lambda x: Row(A=float(x[0]), B=float(x[1]), C=float(x[2]), D=float(x[3]))) 
print randomNumberRdd.take(10)

# create dataframe rdd
schemaRandomNumberDF = spark.createDataFrame(randomNumberRdd)

# print out first 20 lines of dataframe 
#schemaRandomNumberDF.show()

cross_df = schemaRandomNumberDF.crossJoin(schemaRandomNumberDF)
#cross_df.show()

print "----------Count in cross-join--------------- {0}".format(cross_df.count()) 
