from os import environ
from pandas import read_sql
from psycopg2 import connect
from urllib.parse import urlparse

def mt_sql_connect():
    url = urlparse(environ['DATABASE_URL'])

    con = connect(
        dbname = url.path[1:],
        user = url.username,
        password = url.password,
        host = url.hostname,
        port = url.port)

    return(con)

def mt_sql_tags():
    tags = read_sql("SELECT tag FROM tag;",
                    con = mt_sql_connect())['tag'].to_list()

    return(tags)