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

# query = 'SELECT * FROM words'
# words = engine.execute(query)
# for row in words:
#     print(row)


def get_word_details(word):
    word = word.upper()
    result = engine.execute(f"SELECT * FROM words WHERE WORD = '{word}'")
    syllables = 0
    pronunciation = ''
    scansion = ''
    # for item in result:
    #     print(item)
    #     print(type(item))
    result = list(result)[0]
    return result


# def syllable_matches(word):
#     details = get_word_details(word)
#     print(len(details))
#     syllables = details[3]
#     results = engine.execute(f"SELECT * FROM words WHERE SYLLABLES = {syllables}")
#     return [get_word_details(result) for result in results]

def syllable_matches(word):
    details = get_word_details(word)
    syllables = details[3]
    results = engine.execute(f"SELECT * FROM words WHERE SYLLABLES = {syllables}")
    for result in results:
        print(result)

print(get_word_details('empty'))
print(syllable_matches('empty'))