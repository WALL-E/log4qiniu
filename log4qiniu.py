#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
"""download log file from qiniu

Usage:
  qlog.py [-h] [--delay-days=number] [--max-download=number] [-v]
  qlog.py --version

Options:
  --delay-days=1        Days of delayed Download, default is 1
  --max-download=48     The maximum number of log files downloaded, default is 48
  -h --help             show this help message and exit
  -v --verbose          print status messages
  --version             show version and exit

"""

import datetime
import json
import logging
import signal
import os
import sys
from docopt import docopt
import requests
import qiniu

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(filename="/var/log/log4qiniu.log", filemode="a+", format="%(asctime)s-%(name)s-%(levelname)s-%(message)s", level=logging.DEBUG)

delay_days = 1
max_download = 48
verbose = 0
is_exited = False

access_key = ""
secret_key = ""

def onsignal_term(signum, frame):
    global is_exited
    print ("Receive [%s] signal" % (signum))
    is_exited = True

def get_date(days):
    date = datetime.datetime.now() + datetime.timedelta(days=-days)
    return date.strftime('%Y-%m-%d')

def write_disk(path, name, content):
    filename = os.path.join(path, name.replace("v2/.", ""))
    with open(filename, "wb") as code:
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
    logging.debug("log4qiniu starting")
    signal.signal(signal.SIGINT, onsignal_term)
    arguments = docopt(__doc__, version='1.0.0rc1')
    rebuild_options(arguments)

    domains = [".qianbaocard.com"]
    log_date = get_date(delay_days)

    auth = qiniu.Auth(access_key, secret_key)
    cdn = qiniu.CdnManager(auth)
    logging.info("log4qiniu get data %s at %s" % (domains, log_date))
    result = cdn.get_log_list_data(domains, log_date)
    if result[0] is None:
        logging.error("log4qiniu download failed")
        sys.exit(1)

    for v in result[0]["data"].values():
        for log in v[0:max_download]:
            url = log["url"]
            if verbose > 0:
                print "downloading: %s" % (url)
            logging.info("log4qiniu downloading %s" % (url))
            name = log["name"]
            r = requests.get(url)
            write_disk(BASE_DIR, name, r.content)
            if is_exited:
                break

    cmd = "gunzip %s/*.gz" % (BASE_DIR)
    os.system(cmd)

    logging.debug("log4qiniu complate")


if __name__ == '__main__':
    main()
