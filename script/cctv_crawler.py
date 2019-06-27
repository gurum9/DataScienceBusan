import json
import os
import time
from urllib.parse import urlencode

import requests

API_URL = "http://apis.data.go.kr/6260000/busancctvinfoservice/getCctvDetailsInfo"
API_SERVICE_KEY = os.environ['api_key']
API_NUM_OF_ROWS = "100"

getting_page_no = 1
out_cvs_filename = "busancctv_" + time.strftime("%Y%m%d_%H%M%S") + ".csv"


def make_url_string():
    param = {"ServiceKey": API_SERVICE_KEY, "numOfRows": API_NUM_OF_ROWS, "_returnType": "json",\
             "pageNo": getting_page_no}
    get_param = urlencode(param)
    return API_URL + "?ServiceKey=" + API_SERVICE_KEY + "&" + get_param


def save_json(reps_text):
    json_obj = json.loads(reps_text)
    print(f"total count -> {json_obj['totalCount']}")
    print(f"key in item -> {json_obj['list'][0].items()}")

    recv_data_cnt = json_obj['totalCount']

    data_list = json_obj['list']

    k = data_list[0]
    header = ', '.join(k.keys())
    print("헤더값->" + header)

    file_mode = "a" if os.path.exists(out_cvs_filename) else 'w+'

    with open(out_cvs_filename, file_mode, encoding='utf-8') as f:
        if file_mode == 'w+':
            f.write(header + "\n")
        for item in data_list:
            print(','.join(item.values()))
            f.write(','.join('"{0}"'.format(w) for w in item.values()) + "\n")

    return recv_data_cnt


if __name__ == "__main__":
    get_resource_url = make_url_string()
    print(f"request url -> {get_resource_url}")

    reps = requests.get(get_resource_url)
    data_count = save_json(reps.text)
    getting_page_no = getting_page_no + 1

    # 8073 / 100
    req_cnt = round(int(data_count) / int(API_NUM_OF_ROWS))
    for cnt in range(req_cnt - 1):
        get_resource_url = make_url_string()
        print(f"request url -> {get_resource_url}")
        reps = requests.get(get_resource_url)
        save_json(reps.text)
        getting_page_no = getting_page_no + 1
