import os
# import pkg_resources
from flask import *
# from flask_sqlalchemy import SQLAlchemy
from Helper.database import*
# from Helper.app import app
import jinja2
pkg_resources.require("SQLAlchemy==1.3.23")


env = jinja2.Environment()


# Functions to sort through lists returned by database.
def get_syllables_match_list(word: words) -> list:
    """"Searches database for words matching syllable count of input word"""
    results = syllable_matches(word)
    return results


def details_list_to_word_list(list):
    """Converts list of word objects to a list of each word's WORD attribute."""
    return [word.WORD for word in list]


# check if try/except is needed for words not in db
# be sure a dict can be passed to HTML.
# for now, scansion matches will be converted to a single list
def get_exact_matches(word_object: words, syllable_count_matches: list, rhyme_dict: dict, scansion_dict: dict) -> dict:
    """Compares syllable count matches, rhyme matches, and word stress matches
    and returns a list of words found in all three."""
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


# def get_close_matches_rhyme(word_object: words, syllable_count_matches: list) -> dict:
#     """Given a word, searches the database and returns a dict of word objects where
#     rhyme matches are found at various syllable counts."""
#     rhyme_matches = get_rhyme_dict(word_object)
#     close_matches_rhymes = {}
#     # for num in range(word_object.SYLLABLES): # number of syllables
#     for num in range(len(list(rhyme_matches.keys()))): # number of keys, to avoid out of range when matches weren't found.
#         syllable_match_list = details_list_to_word_list(syllable_count_matches)
#         rhyme_list = details_list_to_word_list(rhyme_matches[num + 1])
#         close_matches_rhymes[num+1] = [word for word in syllable_match_list if word in rhyme_list]
#         if len(close_matches_rhymes[num+1]) == 0:
#             close_matches_rhymes.pop(num+1)
#     return close_matches_rhymes





# going to compare performance with working with just the syllable match list
# vs re-querying the database.
def get_close_matches_rhyme(word_object: words, syllable_count_matches: list) -> dict:
    """Given a word, searches the database and returns a dict of word objects where
    rhyme matches are found at various syllable counts."""
    rhyme_matches = get_rhyme_dict(word_object, syllable_count_matches)
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


# the result of forgetting I'd already done the conversion from 0s 1s and 2s -_-
# def convert_stresses(stresses: str) -> str:
#     output = ''
#     for syllable in stresses:
#         output += 'u' if syllable == '0' else "S"
#     return output


# the one function to interact with the website:
# get word_object, get syllable list, get scansion_dict, get rhyme_dict,
# get exact_dict, convert scansion_dict to scansion_set, convert
# scansion, rhyme, and exacts to camel case, and return those!
def all_together_now(word):
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
    stresses = word_object.SCANSION
    # print(type(word_object.SCANSION))
    # print(stresses + "all_together")
    # rhyme_keys = list(exact_dict.keys())
    # for key in rhyme_keys:
    #     print(key)
    #     for word in rhyme_dict[key]:
    #         print(word)
    return [word, syllables, exact_dict, scansion_set, rhyme_dict, stresses]
# above needs syllable count passed in!!!! so we know how long the params will be.


# can 'GET' be passed in to all these functions?! May need to restructure.
@app.route('/results', methods=['POST'])
def search():
    word = request.form['word']
    print(word)
    contents = all_together_now(word)
    word = contents[0]
    syllables = contents[1]
    exact_dict = contents[2]
    scansion_set = contents[3]
    rhyme_dict = contents[4]
    stresses = contents[5]
    return render_template("results.html", word=word, syllables=syllables,
                           exact_dict=exact_dict, scansion_set=scansion_set,
                           rhyme_dict=rhyme_dict, stresses=stresses)
# above needs syllable count passed in!!!! so we know how long the params will be.


@app.route('/<word>')
def word_click(word):
    word = word
    contents = all_together_now(word)
    word = contents[0]
    syllables = contents[1]
    exact_dict = contents[2]
    scansion_set = contents[3]
    rhyme_dict = contents[4]
    stresses = contents[5]
    return render_template("results.html", word=word, syllables=syllables,
                           exact_dict=exact_dict, scansion_set=scansion_set,
                           rhyme_dict=rhyme_dict, stresses=stresses)


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

# print(type(all_together_now('hello')))