import os
import time
from datetime import datetime


def createTimestamp():
    return time.time()


def convertTimestamp(timestamp):
    utc = datetime.utcfromtimestamp(timestamp)
    format = "%a %e %b %Y %r %Z"
    timestamp = utc.strftime(format)
    return timestamp
