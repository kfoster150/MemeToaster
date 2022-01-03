from psycopg2 import connect
from urllib.parse import urlparse
import pandas as pd

DATABASE_URL = "postgres://gwqbhjwinxgpqt:2772bd22425a058877ba93caa2db010a7dfd919ccb6977392597a488af965dc0@ec2-34-232-149-136.compute-1.amazonaws.com:5432/d3tofbie0samkn"

url = urlparse(DATABASE_URL)

con = connect(
    dbname = url.path[1:],
    user = url.username,
    password = url.password,
    host = url.hostname,
    port = url.port
)

tags = pd.read_sql("SELECT tag FROM tag;", con = con)['tag']

print(tags.head())
print(type(tags))

for tag in tags:
    print(tag)