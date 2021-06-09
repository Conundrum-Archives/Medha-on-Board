import os, psutil, json
from time import sleep
import time

filename = "data.json"
if not os.path.exists(filename):
  with open(filename, 'w') as f:
    f.write('{}')
def appendjson(data):
  with open(filename, 'r+') as fl:
    file_data = json.load(fl)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    file_data[timestamp] = data
    fl.seek(0)
    json.dump(file_data, fl, separators=(',', ':'))


while True:
  with open('../rpi/envdetails.json') as ed:
    data = json.load(ed)
    print("pid: {}".format(data["pid"]))

    proc =  psutil.Process(pid=data["pid"])
    net = psutil.net_io_counters()
    cputimes = psutil.cpu_times()


    teldata = {
      "system": {
        # "pids": psutil.pids(),
        "network": {
          "bytessent": net.bytes_sent,
          "bytesrecv": net.bytes_recv,
          "packetssent": net.packets_sent,
          "packetsrecv": net.packets_recv
        },
        "cpu": {
          "cputimes": {
            "user": cputimes.user,
            "system": cputimes.system,
            "idle": cputimes.idle
          }
        }
      },
      "medha": {
        "pid": data["pid"],
        "exist": psutil.pid_exists(data["pid"]),
        "memory": proc.memory_info().rss / 1024**2,
        "cputimes": {
          "user": proc.cpu_times().user,
          "system": proc.cpu_times().system
        },
        "cpupercent": proc.cpu_percent(interval=1)
      }
    }
    appendjson(teldata)
  sleep(1)