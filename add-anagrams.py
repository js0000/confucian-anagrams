# add-anagrams.py
# adds "anagram processed" texts to python data structure

import random
import yaml

## DEBUG
#import pprint
#pp = pprint.PrettyPrinter( indent = 2 )


## SUBROUTINES
def generateAnagramText( vt, rk ):
    return vt

# subroutine only a stub now
# coding logic explained below

# process each verseText using regex
# in case of multiple matches in a string, choose only one to replace
## if 'the Master' exists directly replace
## if one of computed list 
### find string in text and add words on each side until > N length
### do not cross punctuation boundaries
### shuffle anagram words and replace
## else
### select anagram text by looking for long words
### continue as if found long word was computed list string and further lengthen as necessary
# if original text has initial uppercase letter, do the same for replacement


## MAIN

f = open( 'replacementKeys.yaml' )
replacementKeys = yaml.load( f )
f.close()
random.shuffle( replacementKeys['the-Master'] )

f = open( 'raw-analects.yaml' )
analects = yaml.load( f )
f.close()

for book in analects:
    for chapter in book['bookChapters']:
        for verse in chapter['chapterVerses']:
            anagramText = generateAnagramText( verse['verseText'], replacementKeys )

# add 'anagramText' key to verse object
# add 'info' key with date/time of replacement
## also maybe other interesting stats
# dump updated data to yaml


