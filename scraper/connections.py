import psycopg2
import requests
import json
from dotenv import dotenv_values
from requests.auth import HTTPBasicAuth
from datetime import datetime
from time import sleep

try:
    API_AUTHORISATION = HTTPBasicAuth(
        dotenv_values("../.env")["GITHUB_USER"], dotenv_values("../.env")["GITHUB_API_KEY"])
except:
    API_AUTHORISATION = HTTPBasicAuth(
        dotenv_values(".env")["GITHUB_USER"], dotenv_values(".env")["GITHUB_API_KEY"])


def get_database_connection():
    try:
        try:
            database_ip=dotenv_values("../.env")["DATABASE_IP"]
            database_name=dotenv_values("../.env")["DATABASE_NAME"]
            database_user=dotenv_values("../.env")["DATABASE_USER"]
            database_password=dotenv_values("../.env")["DATABASE_PASSWORD"]
        except:
            database_ip=dotenv_values(".env")["DATABASE_IP"]
            database_name=dotenv_values(".env")["DATABASE_NAME"]
            database_user=dotenv_values(".env")["DATABASE_USER"]
            database_password=dotenv_values(".env")["DATABASE_PASSWORD"]
        connection = psycopg2.connect(
            f"dbname='{database_name}' user='{database_user}' host='{database_ip}' password='{database_password}'")
    except psycopg2.OperationalError as ex:
        print(f"Database authentication failed: {repr(ex)}")
        return None
    else:
        return connection

def get_cursor(select_statement) -> object:
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute(select_statement)
        recorset = cursor.fetchall()
    except Exception as ex:
        print(f"Query failed: {repr(ex)}")
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
        print(f"Changes failed to commit: {repr(ex)}")
    finally:
        connection.close()

def wait_for_githup_api_limit(headers):
    try:
        wait_time = (float(headers["X-RateLimit-Reset"]) - datetime.strptime(
            headers["Date"],"%a, %d %b %Y %H:%M:%S GMT").timestamp()) / (float(headers["X-RateLimit-Remaining"]) + 1)
        sleep(wait_time)
    except Exception as ex:
        print(f"API call failed ({headers}): {repr(ex)}")

def get_from_github(url):
    try:
        response = requests.get(url, auth=API_AUTHORISATION)
        wait_for_githup_api_limit(response.headers)
        #print(json.dumps(response.json()))
        return response.json()
    except Exception as ex:
        print(f"API get call failed ({url}): {repr(ex)}")

def get_github_collection_count(url):
    try:
        print(url)
        response = requests.get(f"{url}?per_page=1", auth=API_AUTHORISATION)
        wait_for_githup_api_limit(response.headers)
        try:
            collection_count = int(response.headers["Link"][response.headers["Link"].find("&page=",
                            response.headers["Link"].find("&page=")+1)+6:response.headers["Link"].find(
                            ">;",response.headers["Link"].find(">;")+1)])
        except Exception:
            collection_count = 0 if isinstance(response.json(),type(None)) else len(response.json())
        return collection_count
    except Exception as ex:
        print(f"API count call failed ({url}): " + repr(ex))

def get_github_collection_item(url, item_index):
    try:
        response = requests.get(f"{url}?per_page=1&page={item_index}", auth=API_AUTHORISATION)
        wait_for_githup_api_limit(response.headers)
        return response.json()[0]
    except IndexError as ex:
        pass
    except Exception as ex:
        print(f"API get item call failed ({url}): {repr(ex)}")
