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
  - 
