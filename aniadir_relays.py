import requests
from time import sleep
ID = "10016b7041"


def add_subdevices(IDs):
    data = {"deviceid": IDs, "data": {}}
    url = "http://192.168.2.106:8081/zeroconf/add_sub_devices"
    response = requests.post(url, json=data)
    res = []
 

if __name__ == "__main__":
    add_subdevices(ID)
