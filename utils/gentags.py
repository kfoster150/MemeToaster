# Now that all the pictures are in one folder, it's
# time to add them to the PostGreSQL database, 
# adding tags and relations

# Import libraries
import psycopg2
from urllib.parse import urlparse
import os, re
import pandas as pd

DATABASE_URL = "postgres://gwqbhjwinxgpqt:2772bd22425a058877ba93caa2db010a7dfd919ccb6977392597a488af965dc0@ec2-34-232-149-136.compute-1.amazonaws.com:5432/d3tofbie0samkn"

# Connect to MemeToaster2 Database
url = urlparse(DATABASE_URL)

con = psycopg2.connect(
    dbname = url.path[1:],
    user = url.username,
    password = url.password,
    host = url.hostname,
    port = url.port
)
cur = con.cursor()

def addImage(filename):
    print(filename)
    # Get Existing Data
    tagTable = pd.read_sql("SELECT * FROM tag;", con = con)
    filenameTable = pd.read_sql("SELECT * FROM filename;", con = con)

    # Add tag if not exists
    tag = re.match('[a-zA-Z]+', filename)[0]
    if not tag in tagTable[['tag']].values:
        add_tag_str = f"""INSERT INTO tag(tag) VALUES ('{tag}');"""
        cur.execute(add_tag_str)
    else:
        print(f"`{tag}` already in tag table")

    if not filename in filenameTable[['filename']].values:
        add_filename_str = f"""INSERT INTO filename(filename) VALUES ('{filename}');"""
        cur.execute(add_filename_str)

        # Get tag and filename id
        tagID = pd.read_sql(f"SELECT id FROM tag WHERE tag.tag = '{tag}';", con = con)['id'].values[0]
        filenameID = pd.read_sql(f"SELECT id FROM filename WHERE filename.filename = '{filename}';", con = con)['id'].values[0]

        add_relationship_str = f"""INSERT INTO tag_filename(filename_id, tag_id) VALUES ({filenameID}, {tagID});"""
        cur.execute(add_relationship_str)
    else:
        print(f"`{filename}` already in filename table")

schema_string = """
DROP TABLE IF EXISTS filename;
DROP TABLE IF EXISTS tag;
DROP TABLE IF EXISTS tag_filename;

CREATE TABLE filename (
  id serial PRIMARY KEY, 
  filename varchar(50) NOT NULL,
  nsfw bool DEFAULT FALSE);

CREATE TABLE tag (
  id serial PRIMARY KEY, 
  tag varchar(25) NOT NULL);
 
CREATE TABLE tag_filename (
  id serial PRIMARY KEY,
  filename_id int NOT NULL,
  tag_id int NOT NULL);
"""

cur.execute(schema_string)

DBImageDir = './data/images/db'
filenames = os.listdir(DBImageDir)
filenames.sort()

for filename in filenames:
    addImage(filename)

con.commit()
con.close()
