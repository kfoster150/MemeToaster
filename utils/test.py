from os import environ
from pandas import read_sql
from psycopg2 import connect
from urllib.parse import urlparse

DATABASE_URL = "postgres://gwqbhjwinxgpqt:2772bd22425a058877ba93caa2db010a7dfd919ccb6977392597a488af965dc0@ec2-34-232-149-136.compute-1.amazonaws.com:5432/d3tofbie0samkn"

def mt_sql_connect():
    url = urlparse(DATABASE_URL)

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

print(mt_sql_tags())
print(type(mt_sql_tags()))


if 'angry' in mt_sql_tags():
    print("it here")
else:
    print("it not here")