#!/var/www/html/scripts/bin/python

# Script originally provided by AlekseyP
# https://www.reddit.com/r/technology/comments/43fi39/i_set_up_my_raspberry_pi_to_automatically_tweet/
# modifications by roest - https://github.com/roest01
# additional modifications by hobo05 - https://github.com/hobo05

import os
import csv
import datetime
import time
from speedtest import Speedtest
import logging

#static values
CSV_FIELDNAMES=["timestamp", "ping", "download", "upload"]
FILEPATH = os.path.dirname(os.path.abspath(__file__)) + '/../data/result.csv'

def runSpeedtest():
        logger = logging.getLogger(__name__)

        #run speedtest-cli
        logger.info('--- running speedtest ---')

        #execute speedtest
        try:
                servers = []
                threads = None

                s = Speedtest()
                s.get_servers(servers)
                s.get_best_server()
                s.download(threads=threads)
                s.upload(threads=threads, pre_allocate=False)
                result = s.results.dict()

                #collect speedtest data
                ping = round(result['ping'], 2)
                download = round(result['download'] / 1000 / 1000, 2)
                upload = round(result['upload'] / 1000 / 1000, 2)

                logger.info(f"Ran speedtest...")
        except Exception as e:
                ping = None
                download = 0
                upload = 0
                logger.error(f"Speedtest failed to run with error: {e}")

        # always set timestamp
        timestamp = round(time.time() * 1000, 3)

        csv_data_dict = {
                CSV_FIELDNAMES[0]: timestamp,
                CSV_FIELDNAMES[1]: ping,
                CSV_FIELDNAMES[2]: download,
                CSV_FIELDNAMES[3]: upload}

        #write testdata to file
        isFileEmpty = not os.path.isfile(FILEPATH) or os.stat(FILEPATH).st_size == 0

        with open(FILEPATH, "a") as f:
                csv_writer = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=CSV_FIELDNAMES)
                if isFileEmpty:
                        csv_writer.writeheader()

                csv_writer.writerow(csv_data_dict)

        #log testdata
        ping_as_string = ''
        if ping:
                ping_as_string = "%d" % ping

        logger.info('--- Result ---')
        logger.info("Timestamp: %s" %(timestamp))
        logger.info("Ping: %s [ms]" % (ping_as_string))
        logger.info("Download: %d [Mbit/s]" %(download))
        logger.info("Upload: %d [Mbit/s]" %(upload))

if __name__ == '__main__':
        logging.basicConfig(
                format="%(asctime)s %(levelname)-8s %(message)s",
                level=logging.INFO,
                datefmt="%Y-%m-%d %H:%M:%S")

        runSpeedtest()

        logger = logging.getLogger(__name__)
        logger.info('speedtest complete')
