# functions to get necessary lists from database.
# will make a db Class with functions for each of the word criteria.
# these will return lists
# import sqlalchemy
import pkg_resources
from Helper.app import app
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine, Table
# import re
pkg_resources.require("SQLAlchemy==1.3.23")


db = SQLAlchemy(app)


class words(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    WORD = db.Column(db.Text)
    PRONUNCIATION = db.Column(db.Text)
    SYLLABLES = db.Column(db.Integer)
    SCANSION = db.Column(db.Text)

    def __init__(self, word, pronunciation, syllables, scansion):
        self.WORD = word
        self.PRONUNCIATION = pronunciation
        self.SYLLABLES = syllables
        self.SCANSION = scansion


def get_word_details(word: str) -> words:
    """Pulls word's row from database and returns a tuple of the values"""
    word = word.upper()
    result = words.query.filter(words.WORD == word).first()

    return result


# might not need this, as we can call the word object attributes
def create_word_details_from_object(word_object: words) -> tuple:
    word_details = (word_object.index, word_object.WORD, word_object.PRONUNCIATION, word_object.SYLLABLES, word_object.SCANSION)
    return word_details


def syllable_matches(word_object: words) -> list:
    """Get words from database that match syllable count."""
    results = words.query.filter(words.SYLLABLES == word_object.SYLLABLES, words.WORD != word_object.WORD).all()
    results = sorted(results, key=lambda x: x.WORD)
    return results


# syllables_to_list may be superfluous depending on matching multiple rhymes
# unless it is changed to take in a list.. then it would be reusable
def syllables_to_list(word_object: words) -> list:
    """convert syllables of a word to a list of syllables to use for matching rhymes"""
    # if there is only one syllable, join the entire pronunciation (not including first consonant)
    # if there are multiple... decide how to pair the ARPemes.
    pronunciation = word_object.PRONUNCIATION.split()
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
        if pronunciation_list[i][0] in ['A', 'E', 'I', 'O', 'U']:
            rhyme = ' '.join(pronunciation_list[i:])
            # pronunciation_list = pronunciation_list[:i]
            break
        else:
            i -= 1
    # pronunciation_list.append(rhyme)
    return rhyme

# remember to pop the searched word when presenting the list later.
# def match_syllable(word_object: words, syllable: str) -> list:
#     results = words.query.filter(words.PRONUNCIATION.endswith(syllable), words.WORD != word_object.WORD).all()
#     return  results


def match_syllable(word_object: words, syllable: str, syllable_count_matches: list) -> list:
    # results = words.query.filter(words.PRONUNCIATION.endswith(syllable), words.WORD != word_object.WORD).all()
    results = [word for word in syllable_count_matches if
               word.PRONUNCIATION.endswith(syllable) and word.WORD != word_object.WORD]
    return  results


def get_rhyme_dict(word_object: words, syllable_count_matches: list) -> dict:
    """Given a word, return a dictionary with number of syllables rhymed as the key
    and matching words as values"""
    # this function could also match by syllables to avoid cleaning up later, but eventually
    # I would like an option that lets a user see matching rhymes of variable syllable counts.
    syllable_count = word_object.SYLLABLES
    pronunciation_list = syllables_to_list(word_object)
    rhyme = ''
    results_dict = {}
    i = 0
    while i < syllable_count:
        if i == 0:
            temp = syllable_to_match(pronunciation_list)
            rhyme = temp
            results_dict[i+1] = match_syllable(word_object, rhyme, syllable_count_matches)
            # now have to delete that last syllable from the pronunciation_list
            num_indexes_to_remove = len(temp.split())
            pronunciation_list = pronunciation_list[:-num_indexes_to_remove]
            i += 1
        else:
            temp = syllable_to_match(pronunciation_list)
            rhyme = temp + ' ' + rhyme
            value_list = match_syllable(word_object, rhyme, syllable_count_matches)
            for word in value_list:
                if word in results_dict[i]:
                    results_dict[i].remove(word)
                else:
                    value_list.append(word)
            results_dict[i+1] = value_list
            if len(results_dict[i+1]) == 0:
                results_dict.pop(i+1)
                break
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
def get_scansion_matches(word_object: words) -> dict:
    """Given a word, return words with matching stress pattern. If the word contains
    a secondary stress, return additional keys with the s-stress promoted & demoted"""
    # scansion = word_details[4]
    # syllable_count = word_details[3]
    # double check the rules and how secondary stresses are treated when
    # the unstressesd syllables are in the same word.
    # print(scansion)
    results_dict = {}
    if 's' in word_object.SCANSION:
        scansion_promoted = word_object.SCANSION.replace('s', "p")
        scansion_demoted = word_object.SCANSION.replace('s', 'u')
        results_dict['promoted'] = words.query.filter(words.SCANSION == scansion_promoted).all()
        results_dict['demoted'] = words.query.filter(words.SCANSION == scansion_demoted).all()
    results_dict['exact'] = words.query.filter(words.SCANSION == word_object.SCANSION).all()
    return results_dict


db.init_app(app)
