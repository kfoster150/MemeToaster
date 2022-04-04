from os import environ
from boto3 import Session
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