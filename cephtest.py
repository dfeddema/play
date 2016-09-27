import time
import random
import json
import sys
import os
import errno

import pyspark
from pyspark import SparkContext


endpoint = "10.19.47.70"
access_key = "0ZVTY7QAKJ8UBE3QFO4R"
secret_key = "J3uyfdpH99i4UfzAhYC3sag5XT9M5JuYJKcDjDMr"
settings = [("fs.s3a.endpoint", endpoint), ("fs.s3a.access.key", access_key), ("fs.s3a.secret.key", secret_key), ("fs.s3a.connection.ssl.enabled", "false")]

if __name__ == "__main__": 

     sc = pyspark.SparkContext(appName="S3aTest")
     for k, v in settings:
        sc._jsc.sc().hadoopConfiguration().set(k, v)

     sc.parallelize(range(10000)).saveAsTextFile("s3a://dianes-new-bucket/digits")

     sc.textFile("s3a://dianes-new-bucket/digits").take(5)
     print(repr(sc.textFile("s3a://dianes-new-bucket/digits").take(5)))
# => [u'0', u'1', u'2', u'3', u'4']
