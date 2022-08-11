import database

# Functions to sort through lists returned by database.


def details_list_to_word_list(list):
    return [word[1] for word in list]


    #check if try/except is needed for words not in db
    #be sure a dict can be passed to HTML.
def get_exact_matches(word: str):
    db = database
    word_details = db.get_word_details(word)
    syllable_count_matches = db.syllable_matches(word_details)
    rhyme_matches = db.get_rhyme_dict(word_details)
    scansion_matches = db.get_scansion_matches(word_details)
    exact_matches = {}
    for syllable in range(word_details[3]):
        exact_matches[syllable+1] = []
    pass


# def get_close_matches_rhyme(word: str):
#     db = database
#     word_details = db.get_word_details(word)
#     syllable_count_matches = details_list_to_word_list(database.syllable_matches(word_details))
#     # print(syllable_count_matches)
#     rhyme_matches =
#     rhyme_matches = db.get_rhyme_dict(word_details)
#     # print(rhyme_matches[2])
#     close_matches_rhyme = {}

def get_close_matches_rhyme(word: str) -> dict:
    db = database
    word_details = db.get_word_details(word)
    syllable_count_matches = details_list_to_word_list(db.syllable_matches(word_details))
    rhyme_matches = db.get_rhyme_dict(word_details)
    close_matches_rhymes = {}
    for num in range(word_details[3]): # number of syllables
        rhyme_list = details_list_to_word_list(rhyme_matches[num + 1])
        close_matches_rhymes[num+1] = [word for word in syllable_count_matches if word in rhyme_list]
        # for word in rhyme_matches[2]:
    #     print(word)
    # for syl in range(word_details[3]):
    #     close_matches_rhymes[syl+1] = [word for word in syllable_count_matches if word in rhyme_matches.values()]
    #     # print(close_matches_rhymes[syl+1])
        # comparison_list = rhyme_matches[num+1]
        # print(comparison_list)
        # for word in syllable_count_matches:
        #     print(word)
    # print(close_matches_rhymes)
    return close_matches_rhymes


def get_close_matches_scansion(word: str) -> dict:
    db = database
    word_details = db.get_word_details(word)
    syllable_count_matches = details_list_to_word_list(db.syllable_matches(word_details))
    scansion_matches = db.get_scansion_matches(word_details)
    keys = list(scansion_matches.keys())
    # print(keys)
    close_matches_scansion = {}
    # check length of keys or if searched word has a secondary stress
    for i in range(len(keys)):
        scansion_list = details_list_to_word_list(scansion_matches[keys[i]])
        close_matches_scansion[keys[i]] = [word for word in syllable_count_matches if word in scansion_list]
    return close_matches_scansion


# rhyme_dict = get_close_matches_rhyme('agitated')
# scansion = get_close_matches_scansion('agitated')
print(database.get_word_details('amputated'))
# scansion = get_close_matches_scansion('verify')
# print(scansion)
print(rhyme_dict[3])
print(scansion)
# print(scansion[2])
# print(rhyme_dict)
# print(details_list_to_word_list(database.syllable_matches(database.get_word_details('customary'))))

