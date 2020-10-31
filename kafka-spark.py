import sys
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark_cassandra import CassandraSparkContext, saveToCassandra
from datetime import datetime
import json

if __name__ == "__main__":
    conf = SparkConf().setAppName("sensorDataApp")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("OFF")
    ssc = StreamingContext(sc, 5)

    brokers, topic = sys.argv[1:]
    kvs = KafkaUtils.createDirectStream(ssc, [topic],{"metadata.broker.list": brokers})
    lines = kvs.map(lambda x: json.loads(x[1]))
    sensors = lines.map(lambda y : "Aika: " + str(y['weather'][0]['time']) + " | " + "Lämpötila (C):  " + str(y['weather'][0]['temp']) + " | " + "Tuulen nopeus (m/s):  " + str(y['weather'][0]['windspeed'])+ " | " + "Näkyvyys (km): " + str(y['weather'][0]['visibility']))
    sensors.foreachRDD(lambda x: x.foreach(lambda y: print(y)))
    sensors.pprint()
    rdd = lines.map(lambda x : {"sensor": x['id'], "date": datetime.now().strftime("%d.%m.%y"), "event_time": datetime.now().strftime("%H:%M:%S"), "coord_lat": x['coord']['lat'], "coord_lon": x['coord']$
    rdd.foreachRDD(lambda z: z.saveToMongoDB('mongodb://192.168.1.20:27017/sensordatadb.sensordata'))

    ssc.start()
    ssc.awaitTermination()
