import os
import pkg_resources
from flask import *
from flask_sqlalchemy import SQLAlchemy
import jinja2
pkg_resources.require("SQLAlchemy==1.3.23")

# from Helper.database import database as database
# from Helper.database import db, words
# from Helper.database import words
from Helper.app import app

# this might break it again..
# db = database.db
# Functions to sort through lists returned by database.

db = SQLAlchemy(app)
env = jinja2.Environment()


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
def match_syllable(word_object: words, syllable: str) -> list:
    results = words.query.filter(words.PRONUNCIATION.endswith(syllable), words.WORD != word_object.WORD).all()
    return  results

def get_rhyme_dict(word_object: words) -> dict:
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
            results_dict[i+1] = match_syllable(word_object, rhyme)
            # now have to delete that last syllable from the pronunciation_list
            num_indexes_to_remove = len(temp.split())
            pronunciation_list = pronunciation_list[:-num_indexes_to_remove]
            i += 1
        else:
            # needs a check for if a math is in a prior key, if so... pop it from that earlier key.
            temp = syllable_to_match(pronunciation_list)
            rhyme = temp + ' ' + rhyme
            # results_dict[i + 1] = match_syllable(rhyme)
            value_list = match_syllable(word_object, rhyme)
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


def get_syllables_match_list(word: words) -> list:
    results = syllable_matches(word)
    return results


def details_list_to_word_list(list):
    return [word.WORD for word in list]


    #check if try/except is needed for words not in db
    #be sure a dict can be passed to HTML.
# for now, scansion matches will be converted to a single list
def get_exact_matches(word_object: words, syllable_count_matches: list, rhyme_dict: dict, scansion_dict: dict) -> dict:
    scansion_set = convert_dict_to_set(scansion_dict)
    syllable_count_matches = [word.WORD for word in syllable_count_matches]
    exact_matches = {}
    if word_object.SYLLABLES == len(list(rhyme_dict.keys())):
        for syl in range(word_object.SYLLABLES):
            exact_matches[syl+1] = [word for word in syllable_count_matches if word in scansion_set and word in rhyme_dict[syl+1]]
    else:
        for key in list(rhyme_dict.keys()):
            exact_matches[key] = [word for word in syllable_count_matches if word in scansion_set and word in rhyme_dict[key]]
        # if len(exact_matches[syl+1]) == 0:
        #     exact_matches.pop(syl+1)
    return exact_matches


def get_close_matches_rhyme(word_object: words, syllable_count_matches: list) -> dict:
    # word_details = db.get_word_details(word)
    # syllable_count_matches = details_list_to_word_list(db.syllable_matches(word_details))
    rhyme_matches = get_rhyme_dict(word_object)
    close_matches_rhymes = {}
    # for num in range(word_object.SYLLABLES): # number of syllables
    for num in range(len(list(rhyme_matches.keys()))): # number of keys, to avoid out of range when matches weren't found.
        syllable_match_list = details_list_to_word_list(syllable_count_matches)
        rhyme_list = details_list_to_word_list(rhyme_matches[num + 1])
        close_matches_rhymes[num+1] = [word for word in syllable_match_list if word in rhyme_list]
        if len(close_matches_rhymes[num+1]) == 0:
            close_matches_rhymes.pop(num+1)
    return close_matches_rhymes


def get_close_matches_scansion(word_object: words, syllable_count_matches) -> dict:
    syllable_count_matches = details_list_to_word_list(syllable_count_matches)
    # word_details = db.get_word_details(word)
    # syllable_count_matches = details_list_to_word_list(db.syllable_matches(word_details))
    scansion_matches = get_scansion_matches(word_object)
    keys = list(scansion_matches.keys())
    # print(keys)
    close_matches_scansion = {}
    # check length of keys or if searched word has a secondary stress
    for i in range(len(keys)):
        scansion_list = details_list_to_word_list(scansion_matches[keys[i]])
        close_matches_scansion[keys[i]] = [word for word in syllable_count_matches if word in scansion_list]
    return close_matches_scansion


def convert_dict_to_set(input_dict: dict) -> list:
    output = {word for d_list in input_dict.values() for word in d_list}
    return sorted(output)


def convert_words_to_camel_case(word):
    return word.title()


def convert_list_to_camel_case(input_list: list) -> list:
    output_list = [convert_words_to_camel_case(word) for word in input_list]
    return output_list


def convert_dict_to_camel_case(input_dict: dict) -> dict:
    keys = list(input_dict.keys())
    output_dict = {}
    for key in keys:
        output_dict[key] = [convert_words_to_camel_case(word) for word in input_dict[key]]
    return output_dict


# the one function to interact with the website:
# get word_object, get syllable list, get scansion_dict, get rhyme_dict,
# get exact_dict, convert scansion_dict to scansion_set, convert
# scansion, rhyme, and exacts to camel case, and return those!

# can 'GET' be passed in to all these functions?! May need to restructure.
@app.route('/results/<word>')
def all_together_now(word):
    # word = request.args.get['word', 'asdf']
    word = word
    word_object = get_word_details(word)
    if not word_object:
        word_not_found = 1
        return render_template("results.html", word_not_found=word_not_found, word="No matches found")
    syllables = word_object.SYLLABLES
    syllable_count_list = get_syllables_match_list(word_object)
    rhyme_dict = get_close_matches_rhyme(word_object, syllable_count_list)
    scansion_dict = get_close_matches_scansion(word_object, syllable_count_list)
    # objects for comparison are set!
    exact_dict = get_exact_matches(word_object, syllable_count_list, rhyme_dict, scansion_dict)
    # now to convert scansion dict to a set
    # and convert both dicts and the set to camel case
    rhyme_dict = convert_dict_to_camel_case(rhyme_dict)
    scansion_set = convert_dict_to_set(scansion_dict)
    scansion_set = convert_list_to_camel_case(scansion_set)
    exact_dict = convert_dict_to_camel_case(exact_dict)
    word = convert_words_to_camel_case(word_object.WORD)
    # rhyme_keys = list(exact_dict.keys())
    # for key in rhyme_keys:
    #     print(key)
    #     for word in rhyme_dict[key]:
    #         print(word)
    return render_template("results.html", word=word, syllables=syllables,
                           exact_dict=exact_dict, scansion_set=scansion_set,
                           rhyme_dict=rhyme_dict)
# above needs syllable count passed in!!!! so we know how long the params will be.


@app.route('/')
def index():
    return render_template("homepage.html")


# if __name__ == '__main__':
#     port = int(os.environ["PORT"])
#     app.run(host='0.0.0.0', port=port, debug=True)


# have to create params like: exact_1, exact_2, exact_3
# this... might actually be superfluous. time will tell.
def create_params_from_dict(input_dict, param_name):
    keys = list(input_dict.keys())
    params = {}
    for key in keys:
        params[f'{param_name}_{key}'] = input_dict[key]
    return params


def create_param_from_list(input_list, param_name):
    params = {f'{param_name}': input_list}
    return params


def create_content(exact_dict, rhyme_dict, scansion_set):
    content = {}
    params = ['exact', 'rhyme', 'scansion']
    for param in params:
        pass


db.create_all()
# word_details_1 = (71786, 'LOVE', 'L AH1 V', 1, "'")
# rhyme_dict = get_close_matches_rhyme('agitated')
# scansion = get_close_matches_scansion('agitated')
# print(database.get_word_details('amputated'))
# print(test)
# rhymes = get_close_matches_rhyme(database.get_word_details('automatic'), test)
# print(rhymes)
# print(get_close_matches_scansion((71786, 'LOVE', 'L AH1 V', 1, "'"), get_syllables_match_list("love")))
# scansion = get_close_matches_scansion('verify')
# print(scansion)
# print(rhyme_dict[3])
# print(scansion)
# print(scansion[2])
# print(rhyme_dict)
# print(details_list_to_word_list(database.syllable_matches(database.get_word_details('customary'))))

# test = database.get_word_details('anthology')
# test_list = get_syllables_match_list(test)
# rhyme_dict = get_close_matches_rhyme(test, test_list)
# scansion_dict = get_close_matches_scansion(test, test_list)
# set_list = convert_dict_to_set(scansion_dict)

# print({x for v in scansion_dict.values() for x in v})
# print(scansion_dict.values())
# print(convert_dict_to_set(scansion_dict))
# exact_dict = get_exact_matches(test, test_list, rhyme_dict, scansion_dict)
# print(exact_dict)
# print(exact_dict)
# print(rhyme_dict[3])
# print(scansion_dict)

# print(get_exact_matches(test, get_syllables_match_list(test), rhyme_dict, scansion_dict)[2])

# camel_dict = convert_dict_to_camel_case(rhyme_dict)
# camel_list = convert_list_to_camel_case(set_list)
# # print(test_list)
# print(camel_dict[3])
# # print(scansion_dict['demoted'])
# print(camel_list)

# all_together_now('apology')

# params = create_params_from_dict(rhyme_dict, 'rhyme')
# param_keys = list(params.keys())
# print(param_keys)
# print(params['rhyme_3'])

# params = create_param_from_list(set_list, 'scansion')
# print(params)

# $ python3.9 -m venv venv
# $ source venv/bin/activate
# $ pip install -r requirements.txt
# $ ./run.sh

