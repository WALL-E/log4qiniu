#!/usr/bin/python2.6

#
# Kafka: 10.19.33.244:9092 10.19.40.117:9092
#
import qiniu
import requests
import json

access_key = "Fd2PH4O-MVuRihnRO68kyTAg5agUZ5R_oo3DfxLN"
secret_key = "PqXqGQo6MwyMEr_k9RiJ3e0LNQ0TbRthA7-IBPqQ"

domains = [
".qianbaocard.com",
]
log_date = "2017-06-21"

auth = qiniu.Auth(access_key, secret_key)
cdn = qiniu.CdnManager(auth)
result = cdn.get_log_list_data(domains, log_date)

for v in result[0]["data"].values():
    for log in v:
        url = log["url"]
        name = log["name"]
        r = requests.get(url)
        with open(name.replace("v2/.", ""), "wb") as code:
             code.write(r.content)
