import requests
from bs4 import BeautifulSoup

def get_occupancy():
    URL = "https://lti.library.smu.edu.sg/counter/count.json"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup)
    text = str(soup)
    results = {"lks": "",
                "kgc": "" }
    lks_pos = text.find('"inside": ')
    lks_num = ""
    for i in range(lks_pos+10, len(text)):
        if text[i] != "}":
            lks_num += text[i]
        else:
            break
    results["lks"] = lks_num

    kgc_pos = text.rfind('"inside": ')
    kgc_num = ""
    for i in range(kgc_pos+10, len(text)):
        if text[i] != "}":
            kgc_num += text[i]
        else:
            break
    results["kgc"] = kgc_num

    return results

print(get_occupancy())