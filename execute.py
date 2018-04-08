import logging
import os
import time
import argparse

import exportToExcel
import sendEmail

parser = argparse.ArgumentParser(description='Collects informations about porjects, networks, routers, volumes, images, etc. from divine OpenStack cloud', prog='execute')

parser.add_argument('-d', '--debug', default=os.environ.get('DEBUG', False), action='store_true', help='run in debug mode')

args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s | %(message)s")
else:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s | %(message)s")

logger = logging.getLogger(__name__)


# Execute the programs
try:

    # Export the information to excel file
    exportToExcel.export_to_excel()
    
    # Send Email attachment
    sendEmail.send_email()

except Exception as e:
     logger.exception("Exceptions occured while executing tasks {0}".format(e))


