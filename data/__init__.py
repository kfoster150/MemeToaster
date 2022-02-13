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

def mt_sql_tags(output = "Tuples"):

    query_str = """
SELECT tg.tag, count(tf.filename_id)
FROM tag_filename AS tf
LEFT JOIN tag AS tg
ON tf.tag_id = tg.id
WHERE tg.tag <> ''
GROUP BY tg.tag
ORDER BY count(tf.filename_id) DESC, tg.tag;"""

    tagsDf = read_sql(query_str, con = mt_sql_connect())
    if output == "Tuples":
        tags = zip(tagsDf['tag'], tagsDf['count'])
    elif output == "DataFrame":
        tags = tagsDf.copy()
    else:
        tags = None

    return(tags)