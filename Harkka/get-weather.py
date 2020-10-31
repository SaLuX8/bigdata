import datetime as dt
from fmiopendata.wfs import download_stored_query
import threading
import json
import os
# import pytz

# tz = pytz.timezone('Europe/Helsinki')

def setInterval(func,time):
    e = threading.Event()
    while not e.wait(time):
        func()

def getWeather():
        try:
                # Retrieve the latest hour of data from a bounding box
                end_time = dt.datetime.utcnow()
                start_time = end_time - dt.timedelta(hours=1)
                # Convert times to properly formatted strings
                start_time = start_time.isoformat(timespec="seconds") + "Z"
                # -> 2020-07-07T12:00:00Z
                end_time = end_time.isoformat(timespec="seconds") + "Z"
                # -> 2020-07-07T13:00:00Z

                obs = download_stored_query("fmi::observations::weather::cities::multipointcoverage",
                                args=["starttime=" + start_time,
                                      "endtime=" + end_time])
                latest_tstep = max(obs.data.keys())

                if(obs.data[latest_tstep]['Jyväskylä lentoasema AWOS']):
                    #a=obs.data[latest_tstep]['Jyväskylä lentoasema AWOS']
                    #is_local = "a" in locals()
                    #print(is_local)

                # print(obs.data.keys())
                # print(obs.data[latest_tstep])
                # local_tz = tz.localize(latest_tstep)
                # print(local_tz.strftime('%Y-%m-%d %H:%M:%S %z'))
                print(latest_tstep)
                print("Wind speed",obs.data[latest_tstep]['Jyväskylä lentoasema AWOS']['Wind speed']['value'])
                print("Wind direction",obs.data[latest_tstep]['Jyväskylä lentoasema AWOS']['Wind direction']['value'])
                print("Temperatrure",obs.data[latest_tstep]['Jyväskylä lentoasema AWOS']['Air temperature']['value'])
                print("Visibility",obs.data[latest_tstep]['Jyväskylä lentoasema AWOS']['Horizontal visibility']['value']/1000)

                # print(sorted(obs.data[latest_tstep].keys()))
                # print(obs.data[latest_tstep])

                data = {}
                data['weather'] = []
                data['weather'].append({
                'time': str(latest_tstep),
                'windspeed': obs.data[latest_tstep]['Jyväskylä lentoasema AWOS']['Wind speed']['value'],
                'winddirection': obs.data[latest_tstep]['Jyväskylä lentoasema AWOS']['Wind direction']['value'],
                'temp': obs.data[latest_tstep]['Jyväskylä lentoasema AWOS']['Air temperature']['value'],
                'visibility': obs.data[latest_tstep]['Jyväskylä lentoasema AWOS']['Horizontal visibility']['value']/1000
                })

                with open('weather.json', 'w') as outfile:
                        json.dump(data, outfile)

                os.system("bin/kafka-console-producer.sh --broker-list 192.168.1.18:9092 192.168.1.18:9093 192.168.1.18:9094 --topic weather < weather.json")

        except KeyError:
                print("key error")


setInterval(getWeather,300)
