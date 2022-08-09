# functions to get necessary lists from database.
# will make a db Class with functions for each of the word criteria.
# these will return lists
import sqlalchemy
from sqlalchemy import create_engine, Table

hostname='ZipCoders-MacBook-Pro.local'
dbname='project_of_passion'
uname='nick'
pwd='nick123'

engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host=hostname, db=dbname, user=uname,pw=pwd))
metadata = sqlalchemy.MetaData(bind=engine)
conn = engine.connect()

query = 'SELECT * FROM words'
words = engine.execute(query)
for row in words:
    print(row)


