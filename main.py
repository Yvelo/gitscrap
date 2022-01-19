import requests
import numpy as np
import time
import math
import psycopg2
import requests
import json
from dotenv import dotenv_values
from requests.auth import HTTPBasicAuth
from datetime import datetime
from time import sleep
from pprint import pprint

from tests.basic_test import *

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"GitScrap Welcome - 1"]
    #test_case_2()