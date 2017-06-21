#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
"""download log file from qiniu

Usage:
  qlog.py [-h] [--delay-days=number] [--max-download=number] [-v]
  qlog.py --version

Options:
  --delay-days=1        Days of delayed Download, default is 1
  --max-download=24    The maximum number of log files downloaded, default is 24
  -h --help             show this help message and exit
  -v --verbose          print status messages
  --version             show version and exit

"""

import datetime
import json
from docopt import docopt
import requests
import qiniu


delay_days = -1
max_download = 24
verbose = 0

access_key = "Fd2PH4O-MVuRihnRO68kyTAg5agUZ5R_oo3DfxLN"
secret_key = "PqXqGQo6MwyMEr_k9RiJ3e0LNQ0TbRthA7-IBPqQ"

def get_date(days):
    date = datetime.datetime.now() + datetime.timedelta(days=-days)
    return date.strftime('%Y-%m-%d')

def write_disk(name, content):
    with open(name.replace("v2/.", ""), "wb") as code:
        code.write(content)

def rebuild_options(arguments):
    global delay_days
    global max_download
    global verbose
    if arguments["--delay-days"]:
        delay_days = int(arguments["--delay-days"])
    if arguments["--max-download"]:
        max_download = int(arguments["--max-download"])
    if arguments["--verbose"]:
        verbose += 1

def main():
    arguments = docopt(__doc__, version='1.0.0rc1')
    rebuild_options(arguments)

    domains = [".qianbaocard.com"]
    log_date = get_date(delay_days)

    auth = qiniu.Auth(access_key, secret_key)
    cdn = qiniu.CdnManager(auth)
    result = cdn.get_log_list_data(domains, log_date)

    for v in result[0]["data"].values():
        for log in v[0:max_download]:
            url = log["url"]
            if verbose > 0:
                print "downloading: %s" % (url)
            name = log["name"]
            r = requests.get(url)
            write_disk(name, r.content)

if __name__ == '__main__':
    main()
