import database
from database import words

# Functions to sort through lists returned by database.


# def get_syllables_match_list(word) -> list:
#     db = database
#     word_details = db.get_word_details(word)
#     return db.syllable_matches(word_details)

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
    db = database
    # word_details = db.get_word_details(word)
    # syllable_count_matches = details_list_to_word_list(db.syllable_matches(word_details))
    rhyme_matches = db.get_rhyme_dict(word_object)
    close_matches_rhymes = {}
    for num in range(word_object.SYLLABLES): # number of syllables
        syllable_match_list = details_list_to_word_list(syllable_count_matches)
        rhyme_list = details_list_to_word_list(rhyme_matches[num + 1])
        close_matches_rhymes[num+1] = [word for word in syllable_match_list if word in rhyme_list]
    return close_matches_rhymes


def get_close_matches_scansion(word_object: words, syllable_count_matches) -> dict:
    syllable_count_matches = details_list_to_word_list(syllable_count_matches)
    db = database
    # word_details = db.get_word_details(word)
    # syllable_count_matches = details_list_to_word_list(db.syllable_matches(word_details))
    scansion_matches = db.get_scansion_matches(word_object)
    keys = list(scansion_matches.keys())
    # print(keys)
    close_matches_scansion = {}
    # check length of keys or if searched word has a secondary stress
    for i in range(len(keys)):
        scansion_list = details_list_to_word_list(scansion_matches[keys[i]])
        close_matches_scansion[keys[i]] = [word for word in syllable_count_matches if word in scansion_list]
    return close_matches_scansion


def convert_dict_to_set(input_dict: dict) -> list:
    output = {word for vlist in input_dict.values() for word in vlist}
    return sorted(output)



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

test = database.get_word_details('anthology')
# print(test)
test_list = get_syllables_match_list(test)
rhyme_dict = get_close_matches_rhyme(test, test_list)
scansion_dict = get_close_matches_scansion(test, test_list)
# print({x for v in scansion_dict.values() for x in v})
# print(scansion_dict.values())
# print(convert_dict_to_set(scansion_dict))
# exact_dict = get_exact_matches(test, test_list, rhyme_dict, scansion_dict)
# print(exact_dict)
# print(exact_dict)
# print(rhyme_dict[3])
# print(scansion_dict)
print(get_exact_matches(test, get_syllables_match_list(test), rhyme_dict, scansion_dict))