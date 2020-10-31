import sys
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark_cassandra import CassandraSparkContext, saveToCassandra
from datetime import datetime
import json

if __name__ == "__main__":
    appConf = SparkConf().setAppName("sensorDataApp").set("spark.cassandra.connection.host", "192.168.1.20")
    sc = CassandraSparkContext(conf=appConf)
    sc.setLogLevel("OFF")
    ssc = StreamingContext(sc, 5)

    brokers, topic = sys.argv[1:]
    kvs = KafkaUtils.createDirectStream(ssc, [topic],{"metadata.broker.list": brokers})
    lines = kvs.map(lambda x: json.loads(x[1]))
    lines.pprint()
    sensors = lines.map(lambda y : "Aika: " + str(y['weather'][0]['time']) + " | " + "Lämpötila (C):  " + str(y['weather'][0]['temp']) + " | " + "Tuulen nopeus (m/s):  " + str(y['weather'][0$
    sensors.pprint()
    sensors.foreachRDD(lambda x: x.foreach(lambda y: print(y)))
    sensors.pprint()
    #rdd = lines.map(lambda x : {"sensor": x[0], "date": datetime.now().strftime("%d.%m.%y"), "event_time": datetime.now().strftime("%H:%M:%S"), "coord_lat":x['coord']['lat'],"coord_lon":x['$
    #rdd.foreachRDD(lambda z: z.saveToCassandra("sensordatadb","sensordata"))
    ssc.start()
    ssc.awaitTermination()

