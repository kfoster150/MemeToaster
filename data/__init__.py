
from os import environ, path
from boto3 import Session
from json import loads, dumps
from logging import info
from pandas import DataFrame
from psycopg2 import connect
from random import choice, shuffle
from requests import get
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


def mt_sql_tags(conn, output = "Tuples"):

    query_str = """
SELECT tg.tag, count(tf.filename_id)
FROM tag_filename AS tf
LEFT JOIN tag AS tg
ON tf.tag_id = tg.id
WHERE tg.tag <> ''
GROUP BY tg.tag
ORDER BY count(tf.filename_id) DESC, tg.tag;"""

    with conn.cursor() as curs:
        curs.execute(query_str)
        tags = curs.fetchall()

    if output == "DataFrame":
        tags = DataFrame(tags, columns = ['tag','count'])

    return(tags)


def mt_log_tag(tag, caption, success, conn):

    log_tag_string = """
    INSERT INTO tag_log (tag, caption, success)
    VALUES (%s, %s, %s)"""

    with conn.cursor() as curs:
        curs.execute(log_tag_string, vars = (tag, caption, success))
    conn.commit()


def create_tag_list(conn):

    ##### Create tags list
    tagsList = mt_sql_tags(conn = conn)

    with conn.cursor() as cur:
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

conn = mt_sql_connect()
create_tag_list(conn)
conn.close()


####

def call_thesaurus(tag: str):
    base_url = "https://od-api.oxforddictionaries.com/api/v2"
    url = path.join(base_url, "thesaurus", "en-us", tag.lower())

    r = get(url, headers = {"app_id":environ["THES_APP_KEY"],
                            "app_key":environ["THES_APP_KEY"]})

    # Log thesaurus call results
    info("code {}\n".format(r.status_code))
    info("text \n" + r.text)
    info("json \n" + dumps(r.json()))
    
    data = loads(r.content)

    if "results" in data.keys():
        entries = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['synonyms']
        thes_results = [entry["text"] for entry in entries]
        thes_results = [k for k in thes_results if " " not in k and "-" not in k]
        shuffle(thes_results)
    else:
        thes_results = []

    return(thes_results)


def query_filename_by_tag(tag, conn):
    query_by_tag = """
    SELECT filename FROM filename AS f
        LEFT JOIN tag_filename AS tf
        ON f.id = tf.filename_id
            LEFT JOIN tag
            ON tf.tag_id = tag.id
    WHERE tag.tag = %s;"""

    with conn.cursor() as curs:
        curs.execute(query_by_tag, (tag,))
        images = [im[0] for im in curs.fetchall()]

    imageChoice = choice(images)

    return(imageChoice)


def tag_search(tag, tagSet, conn):

    if tag not in tagSet:
        try:
            thes_results = call_thesaurus(tag)
            thes_matches = set(thes_results).intersection(set(tagSet))
            thes_tag = choice(tuple(thes_matches))
            imageChoice = query_filename_by_tag(thes_tag)
        except IndexError:
            imageChoice = None
    else:
        imageChoice = query_filename_by_tag(tag, conn)
    
    return(imageChoice)

