import os
from collections import defaultdict
import logging
from logging.handlers import RotatingFileHandler
import time
import sys

"""Some Constants"""

gDict = defaultdict(lambda: [])



w = open('uploader-bot.txt','w')
w.truncate(0)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("uploader-bot.txt", maxBytes=50000000, backupCount=10),
        logging.StreamHandler(sys.stdout), #to get sys messages
    ],
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)
BROADCAST_MSG = '''
**Total: {}
Done: {}**
'''
