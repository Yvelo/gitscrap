import psycopg2
import requests
import json
from dotenv import dotenv_values
from requests.auth import HTTPBasicAuth
from datetime import datetime
from time import sleep

def get_database_connection():
    try:
        database_ip=dotenv_values("../.env")["DATABASE_IP"]
        database_name=dotenv_values("../.env")["DATABASE_NAME"]
        database_user=dotenv_values("../.env")["DATABASE_USER"]
        database_password=dotenv_values("../.env")["DATABASE_PASSWORD"]
        connection = psycopg2.connect(f"dbname='{database_name}' user='{database_user}' host='{database_ip}' password='{database_password}'")
    except psycopg2.OperationalError as ex:
        print("Database authentication failed: " + repr(ex))
        return None
    else:
        return connection

def get_cursor(select_statement):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute(select_statement)
        recorset = cursor.fetchall()
    except Exception as ex:
        print("Query failed: " + repr(ex))
    else:
        return recorset
    finally:
        connection.close()

def persist_statements(sql_statements):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        for sql_statement in sql_statements:
            cursor.execute(sql_statement)
        connection.commit()
    except Exception as ex:
        print("Changes failed to commit: " + repr(ex))
    finally:
        connection.close()

def wait_for_githup_api_limit(headers):
    try:
        wait_time = (float(headers["X-RateLimit-Reset"]) - datetime.strptime(headers["Date"],"%a, %d %b %Y %H:%M:%S GMT").timestamp()) / (float(headers["X-RateLimit-Remaining"]) + 1)
        sleep(wait_time)
    except Exception as ex:
        print("API call failed: " + repr(ex))

def get_from_github(url):
    try:
        response = requests.get(url, auth=HTTPBasicAuth(dotenv_values("../.env")["GITHUB_USER"], dotenv_values("../.env")["GITHUB_API_KEY"]))
        json_response = response.json()
        wait_for_githup_api_limit(response.headers)
        #print(json.dumps(json_response))
        return json_response
    except Exception as ex:
        print("API call failed: " + repr(ex))

def get_github_collection_count(url):
    try:
        response = requests.get(f"{url}?per_page=1", auth=HTTPBasicAuth(dotenv_values("../.env")["GITHUB_USER"], dotenv_values("../.env")["GITHUB_API_KEY"]))
        wait_for_githup_api_limit(response.headers)
        if len(response.json())>0:
            collection_count = int(response.headers["Link"][response.headers["Link"].find("&page=",response.headers["Link"].find("&page=")+1)+6:response.headers["Link"].find(">;",response.headers["Link"].find(">;")+1)])
        else:
            collection_count = 0
        return collection_count
    except Exception as ex:
        print("API call failed: " + repr(ex))

def get_github_collection_item(url, item_index):
    try:
        response = requests.get(f"{url}?per_page=100&page={int(item_index/100)}", auth=HTTPBasicAuth(dotenv_values("../.env")["GITHUB_USER"], dotenv_values("../.env")["GITHUB_API_KEY"]))
        json_response = response.json()
        wait_for_githup_api_limit(response.headers)
        return json_response[item_index % 100]
    except Exception as ex:
        print("API call failed: " + repr(ex))
