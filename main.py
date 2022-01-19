from tests.basic_test import *

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"GitScrap Welcome - Test case 2 runing"]
    test_case_2()