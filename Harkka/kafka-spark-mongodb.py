import sys
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from datetime import datetime
import pymongo_spark
import json

pymongo_spark.activate()

def saveAs(rdd):
    if not rdd.isEmpty():
       rdd.saveToMongoDB('mongodb://192.168.1.20:27017/weatherdb.weatherdata')

if __name__ == "__main__":
    conf = SparkConf().setAppName("sensorDataApp")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("OFF")
    ssc = StreamingContext(sc, 300)

    brokers, topic = sys.argv[1:]
    kvs = KafkaUtils.createDirectStream(ssc, [topic],{"metadata.broker.list": brokers})
    lines = kvs.map(lambda x: json.loads(x[1]))
    sensors = lines.map(lambda y : "Aika: " + str(y['weather'][0]['time']) + " | " + "Lämpötila (C):  " + str(y['weather'][0]['temp']) + " | " + "Tuulen nopeus (m/s):  " + str(y['weather'][0]['windspeed']))
    sensors.foreachRDD(lambda x: x.foreach(lambda y: print(y)))
    sensors.pprint()
    rdd = lines.map(lambda x : {"timestamp": datetime.now(),"measuretime": x['weather'][0]['time'], "temp": x['weather'][0]['temp'], "windspeed": x['weather'][0]['windspeed'], "visibility": x['weather'][0]['visibility']})
    rdd.foreachRDD(lambda z: saveAs(z))
    ssc.start()
    ssc.awaitTermination()

