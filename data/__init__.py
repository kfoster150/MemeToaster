from datetime import datetime as dt
from os import environ
from boto3 import Session
from pandas import DataFrame
from psycopg2 import connect
from urllib.parse import urlparse

def mt_sql_connect():
    url = urlparse(environ['DATABASE_URL'])

    conn = connect(
        dbname = url.path[1:],
        user = url.username,
        password = url.password,
        host = url.hostname,
        port = url.port)

    return(conn)


def mt_sql_tags(output = "Tuples", conn = mt_sql_connect(), close = True):

    query_str = """
SELECT tg.tag, count(tf.filename_id)
FROM tag_filename AS tf
LEFT JOIN tag AS tg
ON tf.tag_id = tg.id
WHERE tg.tag <> ''
GROUP BY tg.tag
ORDER BY count(tf.filename_id) DESC, tg.tag;"""

    conn = conn

    with conn.cursor() as curs:
        curs.execute(query_str)
        tags = curs.fetchall()

    if output == "DataFrame":
        tags = DataFrame(tags, columns = ['tag','count'])

    if close:
        conn.close()

    return(tags)


def log_tag(tag, caption, success, conn = mt_sql_connect(), close = True):

    datetime = dt.now().strftime("%Y-%m-%d %H:%M:%S")

    log_tag_string = """
    INSERT INTO tag_log (tag, caption, datetime, success
    VALUES (%s, %s, %s, %s)"""

    with conn.cursor() as curs:
        curs.execute(log_tag_string, vars = (tag, caption, datetime, success))
    conn.commit()

    if close:
        conn.close()


def create_tag_list():
    ##### Create tags list
    tagsList = mt_sql_tags()

    with mt_sql_connect().cursor() as cur:
        cur.execute("SELECT COUNT(id) FROM tag;")
        num_tags = cur.fetchone()[0]
        cur.execute("SELECT COUNT(id) FROM filename;")
        num_pics = cur.fetchone()[0]

    # Write to StringIO, Create S3 session, and upload
    inptstr = 'empty.txt'
    with open(inptstr, 'w') as newfile:

        newfile.write(f"Number of tags: {num_tags}\n\n")
        newfile.write(f"Total number of pictures: {num_pics}\n\n")
        newfile.write("Number of pictures per tag:\n\n")

        for tag, count in tagsList:
            newfile.write(f"{tag}\n{count}\n\n")

    s3 = Session(
        aws_access_key_id = environ['AWS_ACCESS_KEY'],
        aws_secret_access_key = environ['AWS_SECRET_ACCESS_KEY']
    ).resource('s3')

    s3.Bucket('memetoaster').upload_file(inptstr, "tags.txt", ExtraArgs={'ACL': "public-read", 'ContentType': 'text/plain'})