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

word_details = (37610, 'EMPTY', 'EH1 M P T IY0', 2, "'_")


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


def syllable_matches(word_details):
    """Get words from database that match syllable count."""
    # details = get_word_details(word)
    syllables = details[3]
    word = details[1]
    results = engine.execute(f"SELECT * FROM words WHERE SYLLABLES = {syllables} AND WORD <> '{word}'")
    return [result for result in results]


def syllables_to_list(word_details):
    """convert syllables of a word to a list of syllables to use for matching rhymes"""
    pronunciation = word_details[2].split()
    print(pronunciation)

# print(get_word_details('empty'))
# print(syllable_matches('empty'))
# print(get_word_details('empty') in syllable_matches('empty'))
# print(len(syllable_matches('empty')))

syllables_to_list(word_details)