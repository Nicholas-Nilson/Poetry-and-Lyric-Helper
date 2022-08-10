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


def get_word_details(word: str) -> tuple:
    """Pulls word's row from database and returns a tuple of the values"""
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

def syllable_to_match(syllables: int, pronunciation_list: list) -> str:
    """Parses syllables list to find last syllable"""
    # pronunciation_list = syllables_to_list(word_details)
    # print(pronunciation_list)
    # syllables = word_details[3]
    rhyme = ''
    # if there is only 1 syllable, we want from the first vowel sound to the end.
    # or do we -_- this may be able to work the same way forward & back

    i = len(pronunciation_list) - 1
    print(i)
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
            temp = syllable_to_match(syllable_count, pronunciation_list)
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
            temp = syllable_to_match(syllable_count, pronunciation_list)
            rhyme = temp + ' ' + rhyme
            results_dict[i + 1] = match_syllable(rhyme)
            num_indexes_to_remove = len(temp.split())
            pronunciation_list = pronunciation_list[:-num_indexes_to_remove]
            # print(results_dict)
            i += 1
    return results_dict




# def get_rhyme_dict(word_details):
#     """Returns matches in database for each number of syllables in a word"""
#     syllables = word_details[3]
#     pronunciation_list = syllables_to_list(word_details)
#     rhyme = ''
#     results_dict = {}
#     for num in range(syllables):
#         temp = syllable_to_match(syllables, pronunciation_list)
#         indexes_to_remove = len(temp.split())
#         print(pronunciation_list)
#         pronunciation_list = pronunciation_list[:-indexes_to_remove]
#         print(pronunciation_list)
#         rhyme = temp + ' ' + rhyme
#         results_dict[num+1] = match_syllable(rhyme)
#         print('why?')
#         continue
#     return results_dict

    # rhyme = ""
    # pronunciation = word_details[2] # may be unnecessary
    # pronunciation_list = syllables_to_list(word_details) # store the syllable and pop it from list
    # syllables = word_details[3]
    # results_dict = {}
    # # goal here is to return a dictionary with a list of matching words as values, # of matching syllables as the key.
    # # It may be best to start with the most syllable matches as it will be categorized according to it later.
    # # Depending on how I implement this, there can be many repeat words in the multiple keys.
    # for n in range(syllables):
    #     temp = syllable_to_match(word_details)
    #     temp, word_details[2] = temp[::-1], word_details[2][::-1]
    #     print(temp)
    #     rhyme = temp + ' ' + 'rhyme'
    #     results_dict[n+1] = match_syllable(temp)
    # return results_dict





# SELECT * FROM words WHERE PRONUNCIATION LIKE '%AH1 V';

# print(get_word_details('love'))
# print(syllables_to_list(word_details_1))
# print(syllable_matches(word_details))

# making sure
# print(get_word_details('customary') in syllable_matches(word_details))
# print(len(syllable_matches('empty')))

# syllables_to_list(word_details)

# syllable = syllable_to_match(4, syllables_to_list(word_details_4))
# print(syllable)
# print(get_rhyme_dict(word_details_1))
# print(f"%{syllable}")
# print(syllable)
# print(match_syllable(syllable))
# print(syllables_to_list(word_details))

# print(get_word_details('subliminal'))
# print(get_rhyme_dict(word_details_1))

# details = get_word_details('subliminal')
# print(details)
# det_list = syllables_to_list(details)
# det_list = det_list[:-2]
# print(det_list)
# print(syllable_to_match(4, det_list))

dict = get_rhyme_dict(get_word_details('subliminal'))
print(dict[3])
