import requests
import json

def get_occupancy():
    URL = "https://lti.library.smu.edu.sg/counter/count.json"
    page = requests.get(URL).text
    page = json.loads(page)

    results = {"lks": page["lks"]["inside"],
                "kgc": page["kgc"]["inside"] }

    return results

print(get_occupancy())