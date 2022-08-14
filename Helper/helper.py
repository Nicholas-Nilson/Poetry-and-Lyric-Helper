import os

from flask import *
from Helper.database import database as database
from Helper.database import db, words
# from Helper.database import words
from Helper.app import app

# this might break it again..
# db = database.db
# Functions to sort through lists returned by database.

def get_syllables_match_list(word: words) -> list:
    results = database.syllable_matches(word)
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
    for syl in range(word_object.SYLLABLES):
        exact_matches[syl+1] = [word for word in syllable_count_matches if word in scansion_set and word in rhyme_dict[syl+1]]
    return exact_matches


def get_close_matches_rhyme(word_object: words, syllable_count_matches: list) -> dict:
    # word_details = db.get_word_details(word)
    # syllable_count_matches = details_list_to_word_list(db.syllable_matches(word_details))
    rhyme_matches = database.get_rhyme_dict(word_object)
    close_matches_rhymes = {}
    for num in range(word_object.SYLLABLES): # number of syllables
        syllable_match_list = details_list_to_word_list(syllable_count_matches)
        rhyme_list = details_list_to_word_list(rhyme_matches[num + 1])
        close_matches_rhymes[num+1] = [word for word in syllable_match_list if word in rhyme_list]
    return close_matches_rhymes


def get_close_matches_scansion(word_object: words, syllable_count_matches) -> dict:
    syllable_count_matches = details_list_to_word_list(syllable_count_matches)
    # word_details = db.get_word_details(word)
    # syllable_count_matches = details_list_to_word_list(db.syllable_matches(word_details))
    scansion_matches = database.get_scansion_matches(word_object)
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
@app.route('/results/<word>', methods=['GET'])
def all_together_now(word):
    word_object = database.get_word_details(word, word)
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
    return render_template("layout.html")


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