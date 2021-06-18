import psutil
import datetime
import requests
import json
import logging
import time

logging.basicConfig(
                format='%(asctime)-15s - %(levelname)8s - %(module)10s - %(message)s',
                level=logging.DEBUG,
                datefmt='%m/%d/%Y %I:%M:%S.%p',
                handlers=[
                        logging.FileHandler("capture.py.log"),
                        logging.StreamHandler()
                ]
        )
log = logging.getLogger(__name__)

log.info("psut.py started")

class psutilLib:
        def __init__(self):
                pass

        def cputimes(self):
                cpuTimes = psutil.cpu_times()
                retData = {
                        "user": cpuTimes.user,
                        "system": cpuTimes.system,
                        "idle": cpuTimes.idle,
                        "interrupt": cpuTimes.interrupt,
                        "dpc": cpuTimes.dpc
                }
                return retData

        def cpupercent(self):
                return {
                        "cpupercent": psutil.cpu_percent()
                }

        def virtualmemory(self):
                virtualmemory = psutil.virtual_memory()
                retData = {
                        "total": virtualmemory.total,
                        "available": virtualmemory.available,
                        "percent": virtualmemory.percent,
                        "used": virtualmemory.used,
                        "free": virtualmemory.free
                }
                return retData

        def netiocounter(self):
                psu_net = psutil.net_io_counters()
                retData = {
                        "bytes_sent": psu_net.bytes_sent,
                        "bytes_recv": psu_net.bytes_recv,
                        "packets_sent": psu_net.packets_sent,
                        "packets_recv": psu_net.packets_recv
                }
                return retData

        def thermal(self):
                try:
                        psu_thermal = psutil.sensors_temperatures()["cpu_thermal"][0]
                        retData = {}
                        retData = {
                                "current": psu_thermal.current,
                                "high": psu_thermal.high,
                                "critical": psu_thermal.critical
                        }
                except Exception as e:
                        retData = {
                                "error": "temperature sensor not found"
                        }
                return retData

        def collectData(self):
                log.debug("collecting data for telemetry")
                telData = {
                        "timestamp": str(datetime.datetime.now().isoformat()),
                        "cputimes": self.cputimes(),
                        "cpupercent": self.cpupercent(),
                        "virtualmemory": self.virtualmemory(),
                        "netiocounter": self.netiocounter(),
                        "thermal": self.thermal()
                }
                return telData


telemetryAPI = "http://10.0.0.104:5000/api/telemetry"
timegap = 10
pst = psutilLib()

while True:
        telData = pst.collectData()
        log.debug(telData)
        try:
                respData = requests.post(telemetryAPI, data=json.dumps(telData), headers={}).content
                log.debug("telemetry sent successful. Response: %s", respData)
        except Exception as e:
                log.error("could not seld telemetry data to server %s", telemetryAPI)
        time.sleep(timegap)
