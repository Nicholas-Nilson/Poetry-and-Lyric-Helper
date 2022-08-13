# Notes

Project Structure:
- database.py
  - for retrieving items from database
  - will need methods for; syllable count, meter, rhyme
    - separate methods will allow adding options for search down the road 
    - rhyme list, syllable list, meter list (finding multiple words that fit a meter / rhyme?)
- helper.py
  - the functions to parse input and pass to database methods
  - structuring lists:
    - matches all 3
    - matches rhyme
    - matches meter
    - matches syllables
  - dictionary for database phonemes to convert to standard phoneme representation
  - dictionary for meter types
  - function to determine meter based on single or multiple words
    - split(" ") to list, get meter of each word and compare to patterns.. regex?
  - ** would it do to split the dictionaries to another file?

To-Do:
- form the database from available resources.
  - check which sql implementation will allow adding additional columns later (for wordnet synsets or a thesaurus)
  - Choose which phoneme implementation to use from base databases (CMU vs AZ vs converting those to a new one)
  - Update return of lists to dicts, this will allow the code to be more modular in the future if the database gets more columns or if their 
  order ever changes.
  - in list/dict manipulation functions, be sure to remove the base word from the return lists (rhyme dict for 'subliminal' has 'subliminal')
  - decide how to handle words with multiple pronunciations
  - make database & helper functions in to a class?
  - make one more .py file for app.routes.
  - refactor code so it isn't constantly returning the same list/dictionaries repeatedly.

Helper functions to return exact & two different types of close matches.

- incorporate an api in to the search result page for the word passed. the information from the single result api calls can be used for a lot of information
- when passing the dicts to HTML, only the set of scansion_dict needs to be passed.
- rhyme_dict gets passed as it
- exact_matches gets passed as is.'