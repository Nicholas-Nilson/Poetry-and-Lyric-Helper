import pkg_resources
from Helper.app import app
from flask_sqlalchemy import SQLAlchemy
pkg_resources.require("SQLAlchemy==1.3.23")


db = SQLAlchemy(app)


class Words(db.Model):
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


def get_word_details(word: str) -> Words:
    """Pulls word's row from database and returns a tuple of the values"""
    word = word.upper()
    result = Words.query.filter(Words.WORD == word).first()
    return result


def syllable_matches(word_object: Words) -> list:
    """Get words from database that match syllable count."""
    results = Words.query.filter(Words.SYLLABLES == word_object.SYLLABLES, Words.WORD != word_object.WORD).all()
    results = sorted(set(results), key=lambda x: x.WORD)
    return results


def syllables_to_list(word_object: Words) -> list:
    """Convert syllables of a word to a list of syllables to use for matching rhymes"""
    # if there is only one syllable, join the entire pronunciation (not including first consonant)
    pronunciation = word_object.PRONUNCIATION.split()
    return pronunciation


def syllable_to_match(pronunciation_list: list) -> str:
    """Parses syllables list to find last syllable"""
    rhyme = ''
    # if there is only 1 syllable, we want from the first vowel sound to the end.
    # or do we -_- this may be able to work the same way forward & back
    i = len(pronunciation_list) - 1
    while i >= 0:
        # Each element in the pronunciation list that starts with a vowel denotes
        # the start of a new syllable.
        if pronunciation_list[i][0] in ['A', 'E', 'I', 'O', 'U']:
            rhyme = ' '.join(pronunciation_list[i:])
            break
        else:
            i -= 1
    return rhyme


def match_syllable(word_object: Words, syllable: str, syllable_count_matches: list) -> list:
    # results = words.query.filter(words.PRONUNCIATION.endswith(syllable), words.WORD != word_object.WORD).all()
    results = {word for word in syllable_count_matches if
               word.PRONUNCIATION.endswith(syllable) and word.WORD != word_object.WORD}
    return sorted(results, key=lambda x: x.WORD)


def get_rhyme_dict(word_object: Words, syllable_count_matches: list) -> dict:
    """Given a word, return a dictionary with number of syllables rhymed as the key
    and matching words as values"""
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
            i += 1
    return results_dict


def get_scansion_matches(word_object: Words) -> dict:
    """Given a word, return words with matching stress pattern. If the word contains
    a secondary stress, return additional keys with the s-stress promoted & demoted"""
    results_dict = {}
    if 's' in word_object.SCANSION:
        scansion_promoted = word_object.SCANSION.replace('s', "p")
        scansion_demoted = word_object.SCANSION.replace('s', 'u')
        results_dict['promoted'] = Words.query.filter(Words.SCANSION == scansion_promoted).all()
        results_dict['demoted'] = Words.query.filter(Words.SCANSION == scansion_demoted).all()
    results_dict['exact'] = Words.query.filter(Words.SCANSION == word_object.SCANSION).all()
    return results_dict


db.init_app(app)
