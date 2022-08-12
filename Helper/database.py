# functions to get necessary lists from database.
# will make a db Class with functions for each of the word criteria.
# these will return lists
import sqlalchemy
from Helper.app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Table

hostname='ZipCoders-MacBook-Pro.local'
dbname='project_of_passion'
uname='nick'
pwd='nick123'

# engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host=hostname, db=dbname, user=uname,pw=pwd))
db = SQLAlchemy(app)
# metadata = sqlalchemy.MetaData(bind=engine)
# conn = engine.connect()

# query = 'SELECT * FROM words'
# words = engine.execute(query)
# for row in words:
#     print(row)

# word_details_1 = (71786, 'LOVE', 'L AH1 V', 1, "'")
# word_details_2 = (37610, 'EMPTY', 'EH1 M P T IY0', 2, "'_")
# word_details_4 = (27630, 'CUSTOMARY', 'K AH1 S T AH0 M EH2 R IY0', 4, "'_`_")


def get_word_details(word: str) -> tuple:
    """Pulls word's row from database and returns a tuple of the values"""
    word = word.upper()
    result = engine.execute(f"SELECT * FROM words WHERE WORD = '{word}'")
    # seeing how to work with LegacyRow object
    # for item in result:
    #     print(item)
    #     print(type(item))
    result = list(result)[0]
    return result


def syllable_matches(word_details: tuple) -> list:
    """Get words from database that match syllable count."""
    # details = get_word_details(word)
    syllables = word_details[3]
    word = word_details[1]
    results = engine.execute(f"SELECT * FROM words WHERE SYLLABLES = {syllables} AND WORD <> '{word}'")
    return [result for result in results]


# syllables_to_list may be superfluous depending on matching multiple rhymes
# unless it is changed to take in a list.. then it would be reusable
def syllables_to_list(word_details: tuple) -> list:
    """convert syllables of a word to a list of syllables to use for matching rhymes"""
    # if there is only one syllable, join the entire pronunciation (not including first consonant)
    # if there are multiple... decide how to pair the ARPemes.
    pronunciation = word_details[2].split()
    # print(pronunciation)
    return pronunciation


# def syllable_to_match(word_details) -> str:
#     """Parses syllables list to find last syllable"""
#     pronunciation_list = syllables_to_list(word_details)
#     # print(pronunciation_list)
#     syllables = word_details[3]
#     rhyme = ''
#     # if there is only 1 syllable, we want from the first vowel sound to the end.
#     # or do we -_- this may be able to work the same way forward & back
#     if syllables == 1:
#         i = 0
#         while i < len(pronunciation_list):
#             if pronunciation_list[i][-1].isdigit():
#                 rhyme = ' '.join(pronunciation_list[i:])
#                 # can use this when matching multiple syllables, for now only a string is needed
#                 # pronunciation_list = pronunciation_list[:i]
#                 break
#             else:
#                 i += 1
#     # for multiple syllables, we need to get the string value of the final syllable.
#     else:
#         i = len(pronunciation_list) - 1
#         while i >= 0:
#             if pronunciation_list[i][-1].isdigit():
#                 rhyme = ' '.join(pronunciation_list[i:])
#                 # pronunciation_list = pronunciation_list[:i]
#                 break
#         else:
#             i -= 1
#     # pronunciation_list.append(rhyme)
#     return rhyme

# def syllable_to_match(syllables: int, pronunciation_list: list) -> str:
#     """Parses syllables list to find last syllable"""
#     # pronunciation_list = syllables_to_list(word_details)
#     # print(pronunciation_list)
#     # syllables = word_details[3]
#     rhyme = ''
#     # if there is only 1 syllable, we want from the first vowel sound to the end.
#     # or do we -_- this may be able to work the same way forward & back
#     if syllables == 1:
#         i = 0
#         while i < len(pronunciation_list):
#             if pronunciation_list[i][-1].isdigit():
#                 rhyme = ' '.join(pronunciation_list[i:])
#                 # can use this when matching multiple syllables, for now only a string is needed
#                 # pronunciation_list = pronunciation_list[:i]
#                 break
#             else:
#                 i += 1
#     # for multiple syllables, we need to get the string value of the final syllable.
#     else:
#         i = len(pronunciation_list) - 1
#         while i >= 0:
#             if pronunciation_list[i][-1].isdigit():
#                 rhyme = ' '.join(pronunciation_list[i:])
#                 # pronunciation_list = pronunciation_list[:i]
#                 break
#         else:
#             i -= 1
#     # pronunciation_list.append(rhyme)
#     return rhyme

def syllable_to_match(pronunciation_list: list) -> str:
    """Parses syllables list to find last syllable"""
    # pronunciation_list = syllables_to_list(word_details)
    # print(pronunciation_list)
    # syllables = word_details[3]
    rhyme = ''
    # if there is only 1 syllable, we want from the first vowel sound to the end.
    # or do we -_- this may be able to work the same way forward & back

    i = len(pronunciation_list) - 1
    while i >= 0:
        if pronunciation_list[i][-1].isdigit():
            rhyme = ' '.join(pronunciation_list[i:])
            # pronunciation_list = pronunciation_list[:i]
            break
        else:
            i -= 1
    # pronunciation_list.append(rhyme)
    return rhyme


# remember to pop the searched word when presenting the list later.
def match_syllable(syllable: str) -> list:
    # results = engine.execute("""SELECT * FROM words WHERE PRONUNCIATION LIKE %s""", {syllable})
    results = engine.execute(f"SELECT * FROM words WHERE PRONUNCIATION LIKE '%%{syllable}'")
    return [result for result in results]


def get_rhyme_dict(word_details):
    syllable_count = word_details[3]
    pronunciation_list = syllables_to_list(word_details)
    rhyme = ''
    results_dict = {}
    i = 0
    while i < syllable_count:
        if i == 0:
            temp = syllable_to_match(pronunciation_list)
            # print(temp)
            rhyme = temp
            results_dict[i+1] = match_syllable(rhyme)
            # print(results_dict)
            # now have to delete that last syllable from the pronunciation_list
            num_indexes_to_remove = len(temp.split())
            # print(num_indexes_to_remove)
            pronunciation_list = pronunciation_list[:-num_indexes_to_remove]
            # print(pronunciation_list)
            i += 1
        else:
            temp = syllable_to_match(pronunciation_list)
            rhyme = temp + ' ' + rhyme
            results_dict[i + 1] = match_syllable(rhyme)
            num_indexes_to_remove = len(temp.split())
            pronunciation_list = pronunciation_list[:-num_indexes_to_remove]
            # print(results_dict)
            i += 1
    return results_dict


# to work with this, I think I will return a dict of promoted & unpromoted secondary stress matches.
# that way the functionality is better prepped for comparing multiple words.
# for now, the two dict keys can either be made in to one set,
# or a distinction can be made upon display w/ the general rule for secondary stresses
# presented (promoted if surrounded by unstressed syllables)
def get_scansion_matches(word_details):
    scansion = word_details[4]
    syllable_count = word_details[3]
    # double check the rules and how secondary stresses are treated when
    # the unstressesd syllables are in the same word.
    # print(scansion)
    results_dict = {}
    if 's' in scansion:
        scansion_promoted = scansion.replace('s', "p")
        scansion_demoted = scansion.replace('s', 'u')
        # print(scansion_promoted)
        # print(scansion_demoted)
        results_dict['promoted'] = [result for result in engine.execute(
            f"SELECT * FROM words WHERE SCANSION LIKE '%%{scansion_promoted}' AND SYLLABLES = {syllable_count}")]
        results_dict['demoted'] = [result for result in engine.execute(
            f"SELECT * FROM words WHERE SCANSION LIKE '%%{scansion_demoted}' AND SYLLABLES = {syllable_count}")]
    results_dict['exact'] = [result for result in engine.execute(f"SELECT * FROM words WHERE SCANSION LIKE '%%{scansion}' AND SYLLABLES = {syllable_count}")]
    return results_dict

    # results = engine.execute(f"SELECT * FROM words WHERE PRONUNCIATION LIKE '{syllable}'")

# SELECT * FROM words WHERE PRONUNCIATION LIKE '%AH1 V';

# print(get_word_details('love'))
# print(syllables_to_list(word_details_1))
# print(syllable_matches(word_details))

# making sure
# print(get_word_details('customary') in syllable_matches(word_details))
# print(len(syllable_matches('empty')))

# syllables_to_list(word_details)


# dict = get_rhyme_dict(get_word_details('helper'))
# print(dict[1])

# details = get_word_details('ulterior')
# print(get_scansion_matches(details)['exact'])

# print(get_word_details('criminal'))

# print(get_scansion_matches(get_word_details('helper')))
# scansion = get_scansion_matches(get_word_details('verify'))
# scansion = get_scansion_matches(get_word_details('tainted'))
# print(scansion.keys())
# print(scansion['promoted'])
# print(scansion['demoted'])
# print(scansion['exact'])
# print(scansion.keys())