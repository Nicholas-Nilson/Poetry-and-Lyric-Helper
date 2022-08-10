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

word_details_1 = (71786, 'LOVE', 'L AH1 V', 1, "'")
word_details_2 = (37610, 'EMPTY', 'EH1 M P T IY0', 2, "'_")
word_details_4 = (27630, 'CUSTOMARY', 'K AH1 S T AH0 M EH2 R IY0', 4, "'_`_")


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
    syllables = word_details[3]
    word = word_details[1]
    results = engine.execute(f"SELECT * FROM words WHERE SYLLABLES = {syllables} AND WORD <> '{word}'")
    return [result for result in results]


def syllables_to_list(word_details):
    """convert syllables of a word to a list of syllables to use for matching rhymes"""
    # if there is only one syllable, join the entire pronunciation (not including first consonant)
    # if there are multiple... decide how to pair the ARPemes.
    pronunciation = word_details[2].split()
    # print(pronunciation)
    return pronunciation


def syllable_to_match(word_details):
    pronunciation_list = syllables_to_list(word_details)
    # print(pronunciation_list)
    syllables = word_details[3]
    rhyme = ''
    # if there is only 1 syllable, we want from the first vowel sound to the end.
    if syllables == 1:
        i = 0
        while i < len(pronunciation_list):
            if pronunciation_list[i][-1].isdigit():
                rhyme = ' '.join(pronunciation_list[i:])
                # can use this when matching multiple syllables, for now only a string is needed
                # pronunciation_list = pronunciation_list[:i]
                break
            else:
                i += 1
    # for multiple syllables, we need to get the string value of the final syllable.
    else:
        i = len(pronunciation_list) -1
        while i >=0:
            if pronunciation_list[i][-1].isdigit():
                rhyme = ' '.join(pronunciation_list[i:])
                # pronunciation_list = pronunciation_list[:i]
                break
        else:
            i -= 1
    # pronunciation_list.append(rhyme)
    return rhyme


def match_syllable(syllable: str):
    # results = engine.execute("""SELECT * FROM words WHERE PRONUNCIATION LIKE %s""", {syllable})
    results = engine.execute(f"SELECT * FROM words WHERE PRONUNCIATION LIKE '%%{syllable}'")
    return [result for result in results]

# SELECT * FROM words WHERE PRONUNCIATION LIKE '%AH1 V';

# print(get_word_details('love'))
# print(syllables_to_list(word_details_1))
# print(syllable_matches(word_details))

# making sure
# print(get_word_details('customary') in syllable_matches(word_details))
# print(len(syllable_matches('empty')))

# syllables_to_list(word_details)

syllable = syllable_to_match(word_details_4)
print(syllable)
# print(f"%{syllable}")
# print(syllable)
print(match_syllable(syllable))
# print(syllables_to_list(word_details))