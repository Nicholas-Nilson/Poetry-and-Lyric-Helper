from flask import *
from Helper.database import*
import jinja2
pkg_resources.require("SQLAlchemy==1.3.23")


env = jinja2.Environment()


# Functions to sort through lists returned by database.
def get_syllables_match_list(word: Words) -> list:
    """"Searches database for words matching syllable count of input word"""
    results = syllable_matches(word)
    return results


# Used for initial tested of dB connection
def details_list_to_word_list(input_list):
    """Converts list of word objects to a list of each word's WORD attribute."""
    return [word.WORD for word in input_list]


# Utilizes functions below to return a list of the various pattern matches
# A dict of exact matches (stresses & rhyme, bases on # of syllables rhymed)
def get_exact_matches(word_object: Words, syllable_count_matches: list, rhyme_dict: dict, scansion_dict: dict) -> dict:
    """Compares syllable count matches, rhyme matches, and word stress matches
    and returns a list of words found in all three."""
    scansion_set = convert_dict_to_set(scansion_dict)
    syllable_count_matches = [word.WORD for word in syllable_count_matches]
    exact_matches = {}
    # Logic to account for words with empty keys. Empty keys occur when
    # a particular word has 5 syllables, for example, and the only words that
    # match 2 syllable rhymes, also match 3 syllable rhymes.
    if word_object.SYLLABLES == len(list(rhyme_dict.keys())):
        for syl in range(word_object.SYLLABLES):
            exact_matches[syl+1] = [word for word in syllable_count_matches
                                    if word in scansion_set and word in rhyme_dict[syl+1]]
    else:
        for key in list(rhyme_dict.keys()):
            exact_matches[key] = [word for word in syllable_count_matches
                                  if word in scansion_set and word in rhyme_dict[key]]
            # If there are no matches, we do not need the key. This helps with
            # keeping the web page clean later.
            if len(exact_matches[key]) == 0:
                exact_matches.pop(key)
    return exact_matches

# Function used when rhyme matches were found in the database and not
# the words matching syllable count. Kept here in the event words of different
# syllable counts are ever wanted for the project.

# def get_close_matches_rhyme(word_object: words, syllable_count_matches: list) -> dict:
#     """Given a word, searches the database and returns a dict of word objects where
#     rhyme matches are found at various syllable counts."""
#     rhyme_matches = get_rhyme_dict(word_object)
#     close_matches_rhymes = {}
#     number of keys, to avoid out of range when matches weren't found.
#     for num in range(len(list(rhyme_matches.keys()))):
#         syllable_match_list = details_list_to_word_list(syllable_count_matches)
#         rhyme_list = details_list_to_word_list(rhyme_matches[num + 1])
#         close_matches_rhymes[num+1] = [word for word in syllable_match_list if word in rhyme_list]
#         if len(close_matches_rhymes[num+1]) == 0:
#             close_matches_rhymes.pop(num+1)
#     return close_matches_rhymes


def get_close_matches_rhyme(word_object: Words, syllable_count_matches: list) -> dict:
    """Given a word, searches the database and returns a dict of word objects where
    rhyme matches are found at various syllable counts."""
    rhyme_matches = get_rhyme_dict(word_object, syllable_count_matches)
    close_matches_rhymes = {}
    # number of keys, to avoid out of range when matches weren't found
    for num in range(len(list(rhyme_matches.keys()))):
        syllable_match_list = details_list_to_word_list(syllable_count_matches)
        rhyme_list = details_list_to_word_list(rhyme_matches[num + 1])
        close_matches_rhymes[num+1] = {word for word in syllable_match_list if word in rhyme_list}
        if len(close_matches_rhymes[num+1]) == 0:
            close_matches_rhymes.pop(num+1)
    return close_matches_rhymes


def get_close_matches_scansion(word_object: Words, syllable_count_matches) -> dict:
    """Compares the syllable stresses of the search word to those found in
    the syllable match list and returns a dict.

    Promoted and demoted keys not yet in use, intended for future
    use when figuring out the scansion of a full line and finding words that
    work in the context of an entire line."""
    results_dict = {}
    if 's' in word_object.SCANSION:
        scansion_promoted = word_object.SCANSION.replace('s', "p")
        scansion_demoted = word_object.SCANSION.replace('s', 'u')
        results_dict['promoted'] = {word.WORD for word in syllable_count_matches if word.SCANSION == scansion_promoted}
        results_dict['demoted'] = {word.WORD for word in syllable_count_matches if word.SCANSION == scansion_demoted}
    results_dict['exact'] = {word.WORD for word in syllable_count_matches if word.SCANSION == word_object.SCANSION}
    return results_dict


def convert_dict_to_set(input_dict: dict) -> list:
    """Flattens a dictionary in to a set.
    Is currently used to convert scansion matches dict to a single set."""
    output = {word for d_list in input_dict.values() for word in d_list}
    return sorted(output)


def convert_words_to_camel_case(word):
    """Converts a string to camel case."""
    return word.title()


def convert_list_to_camel_case(input_list: list) -> set:
    """Converts a list of strings and converts each to camel case."""
    output_set = {convert_words_to_camel_case(word) for word in input_list}
    return output_set


def convert_dict_to_camel_case(input_dict: dict) -> dict:
    """Takes a dict of strings and returns each string to camel case."""
    keys = list(input_dict.keys())
    output_dict = {}
    for key in keys:
        output_dict[key] = sorted({convert_words_to_camel_case(word) for word in input_dict[key]})
    return output_dict


def all_together_now(word):
    """Given a word, finds all exact matches, rhyme matches, and stress
    pattern matches and returns a list."""
    word = word
    word_object = get_word_details(word)
    if word_object is None:
        return None
    else:
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
        return [word, syllables, exact_dict, scansion_set, rhyme_dict, stresses]


@app.route('/results', methods=['POST'])
def search():
    """Function to take a word from the searh bar and return the results
    page when a word is found, and the No Results page if the word is
    not in the database."""
    word = request.form['word']
    contents = all_together_now(word)
    if contents is None:
        return render_template("no_result.html")
    else:
        word = contents[0]
        syllables = contents[1]
        exact_dict = contents[2]
        scansion_set = contents[3]
        rhyme_dict = contents[4]
        stresses = contents[5]
        word_not_found = False
        return render_template("results.html", word=word, syllables=syllables,
                               exact_dict=exact_dict, scansion_set=scansion_set,
                               rhyme_dict=rhyme_dict, stresses=stresses,
                               word_not_found=word_not_found)


@app.route('/<word>')
def word_click(word):
    """Allows result words to be clickable, to find their matches. Most useful
    for clicking on words that only match stress patterns."""
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


db.create_all()


"""
Code written before pass
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
"""
