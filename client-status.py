"""
Description:
    This script will pull the Client details for all devices deployed within
    the tenant.
    The output will be a CSV file that will conatin the following columns-
    Hostname | Username | OS | OS Version | Classification Status |
    Last Event | Actor | Last Event Time
    The output will be available in a file titled 'Clients.csv'

Requirements:
    python 2.7
    requests

To install requests use:
    pip install requests

Usage of program:
    python client-status.py <Tenant-name> <API Token>

Logging:
    All log events generated will be stored in the log file 'client-status.log'
    If there are any issues, please check the log file for details.
    In the event of further assistance please reach out to support@netskope.com
"""
from requests.packages.urllib3 import Retry
from time import strftime, localtime


import logging
import requests
import csv
import sys

THRESHOLD = 500
outfile = "Clients.csv"
LOG_FILENAME = 'client-status.log'


def getClient(tenant, token):
    logger = logging.getLogger("client-status.getClient")
    url = "https://{}.goskope.com/api/v1/clients".format(tenant)
    para = {}
    para['token'] = token
    s = requests.Session()
    https_retries = Retry(total=5, status_forcelist=[500, 503, 504],
                          backoff_factor=0.2)
    https = requests.adapters.HTTPAdapter(max_retries=https_retries)
    s.mount('https://', https)
    records = THRESHOLD
    total = 0
    para['limit'] = THRESHOLD
    skip = 0
    with open(outfile, 'w')as ofile:
        writer = csv.writer(ofile, delimiter=",")
        writer.writerow(["Hostname", "Username", "OS", "OS Version",
                        "Classification Status", "Last Event", "Actor",
                         "Last Event Time"])
        while records == THRESHOLD:
            try:
                response = s.get(url, params=para)
                if response.status_code != 200:
                    logger.error("Status: {}\nProblem with request. Exiting"
                                 .format(response.status_code))
                    logger.error(response.content)
                    sys.exit()
                client_data = response.json()
                try:
                    for client in client_data["data"]:
                        row = [client["attributes"]["host_info"]["hostname"].
                               encode('utf-8'),
                               client["attributes"]["users"][0].get(
                               "username", "").encode('utf-8'),
                               client["attributes"]["host_info"]["os"],
                               client["attributes"]["host_info"]["os_version"],
                               client["attributes"]["users"][0]
                               ["device_classification_status"],
                               client["attributes"]["last_event"]["status"],
                               client["attributes"]["last_event"]["actor"],
                               strftime('%Y-%m-%d %H:%M:%S', localtime(
                                client["attributes"]["last_event"]["timestamp"]
                                ))]
                        writer.writerow(row)
                except KeyError as e:
                    logger.error("Key {} not found skipping record".format(e))
                records = len(client_data["data"])
                total += records
                skip += THRESHOLD
                para.update({'skip': skip})
                logger.info("Total records fetched {}.".format(total))
            except requests.HTTPError as e:
                logger.error(e)
                sys.exit()


def main():
    logger = logging.getLogger("client-status")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(LOG_FILENAME)
    formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-'
                                  '%(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info("Staring script execution")
    if len(sys.argv) != 3:
        print("""Please provide the correct parameters. Usage:\n
        python {} <Tenant-name> <API Token>""".format(sys.argv[0]))
        sys.exit()
    try:
        getClient(sys.argv[1], sys.argv[2])
    except Exception as e:
        logger.error(e)
    logger.info("Script execution complete")


if __name__ == '__main__':
    main()
