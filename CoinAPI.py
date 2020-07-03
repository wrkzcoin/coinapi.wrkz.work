from aiohttp import web
import json
import sys, traceback
import aiohttp, asyncio
import time

# For some environment variables
import os, redis, re

# MySQL
import pymysql, pymysqlpool
import pymysql.cursors

redis_pool = None
redis_conn = None

def init():
    global redis_pool
    print("PID %d: initializing redis pool..." % os.getpid())
    redis_pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True, db=0)


pymysqlpool.logger.setLevel('DEBUG')
myconfig = {
    'host': os.getenv('MYSQL_HOST_COINAPI', 'default_host'),
    'user': os.getenv('MYSQL_USERNAME_COINAPI', 'default_user'),
    'password': os.getenv('MYSQL_PASSWORD_COINAPI', 'default_password'),
    'database': os.getenv('MYSQL_DATABASE_COINAPI', 'default_db'),
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit':True
    }

connPool = pymysqlpool.ConnectionPool(size=4, name='connPool', **myconfig)
conn = connPool.get_connection(timeout=10, retry_num=2)


def openConnection():
    global conn, connPool
    try:
        if conn is None:
            conn = connPool.get_connection(timeout=10, retry_num=2)
        conn.ping(reconnect=True)  # reconnecting mysql
    except:
        print("ERROR: Unexpected error: Could not connect to MySql instance.")
        sys.exit()


async def check_header(secret_key: str):
    return


async def handle_get_all(request):
    uri = str(request.rel_url).lower()
    if uri.startswith('/info/'):
        # /info/coin
    elif uri.startswith('/info'):
        # /info
    elif uri.startswith('/balances/'):
        # /balances/coin | need authorize
    elif uri.startswith('/balances'):
        # /balances | need authorize
    elif uri.startswith('/deposits/'):
        # /deposits/coin | need authorize
    elif uri.startswith('/deposits'):
        # /deposits | need authorize
    elif uri.startswith('/transactions/'):
        # /transactions/coin | need authorize
    elif uri.startswith('/transactions'):
        # /transactions | need authorize
    else:
        return await respond_bad_request()


async def handle_post_all(request):
    uri = str(request.rel_url).lower()
    if uri.startswith('/transactions/send'):
        # /transactions/send | need authorize
    else:
        return await respond_bad_request()


async def respond_unauthorized_request():
    text = "Unauthorized"
    return web.Response(text=text, status=401)


async def respond_bad_request():
    text = "A parse error occured, or an error occured processing your request."
    return web.Response(text=text, status=400)


async def respond_internal_error():
    text = 'An exception was thrown whilst processing the request. Please report.'
    return web.Response(text=text, status=500)


app = web.Application()

app.router.add_route('GET', '/{tail:.*}', handle_get_all)
app.router.add_route('POST', '/{tail:.*}', handle_post_all)

web.run_app(app, host='127.0.0.1', port=6666)
