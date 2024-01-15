import requests
from time import sleep
ID = "10016b7041"

def get_subdivices(_id):
    url = "http://192.168.2.106:8081/zeroconf/subDevList"
    data = {
        "deviceid": _id,
        "data": {
            "ops_mode": "ewelink"
        }
    }
    response = requests.post(url, json=data)
    res = []
    if not response.ok:
        return res
    try:
        res = [z["subDevId"] for z in response.json()["data"]["subDevList"]]
    except:
        pass
    return res

def on_all_switches(_id, sub_devices):
    url = url = "http://192.168.2.106:8081/zeroconf/switches"
    for sub_device in sub_devices:
        data = {
            "deviceid": _id,
            "data": {
                "subDevId": sub_device,
                "switches": [
                    {
                        "switch": "on",
                        "outlet": 0
                    },
                    {
                        "switch": "on",
                        "outlet": 1
                    },
                    {
                        "switch": "on",
                        "outlet": 2
                    },
                    {
                        "switch": "on",
                        "outlet": 3
                    }
                ]
            }
        }
        try:
            requests.post(url, json=data)
        except:
            pass

def get_historical_data (_id, sub_divices):
    url  = "http://192.168.2.106:8081/zeroconf/historicalData"
    for sub_device in sub_devices:
        for i in range(4):
            data = {
                "deviceid": _id,
                "data": {
                    "subDevId": sub_device,
                    "outlet": i,
                    "dateStart": "2023-05-30 18:00",
                    "dateEnd": "2023-05-30 19:10"
                }
            }
            try:
                response = requests.post(url, json=data)
                print (data)
                print (response.content)
                print ()
            except:
                return None


def get_monitor_values(_id, sub_devices):
    url  = "http://192.168.2.106:8081/zeroconf/monitor"
    for sub_device in sub_devices:
        for i in range(4):
            data = {
                "deviceid": ID,
                "data": {
                    "url": "http://192.168.2.105/",
                    "port": 9000,
                    "subDevId": sub_device,
                    "outlet": i,
                    "time":2
                }
            }
            try:
                response = requests.post(url, json=data)
                print (response.content)
                print ()
                sleep(2)
            except:
                return None

if __name__ == "__main__":
    sub_devices = get_subdivices(ID)
    on_all_switches(ID, sub_devices)
    sleep(1)
    get_monitor_values(ID, sub_devices)
    #get_historical_data(ID, sub_devices)

