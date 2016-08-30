# add-anagrams.py
# adds "anagram processed" texts to python data structure

import random
import re
import yaml

## DEBUG
import pprint
#pp = pprint.PrettyPrinter( indent = 2 )


## SUBROUTINES
def replaceMaster( vt, replacement ):
    masterAtStart = False
    n = re.search( '^the master', vt, re.IGNORECASE )
    if n:
        masterAtStart = True

    m = re.split( 'the master', vt, flags=re.IGNORECASE )
    processedVerse = False
    parts = len( m )
    if parts == 0:
        print( 'split fails for ' + vt )
        return False
    # start or end
    elif parts == 1:
        if masterAtStart:
            processedVerse = replacement + ' ' + m[0]
        else:
            processedVerse = m[0] + ' ' + replacement
        
    elif parts == 2:
        processedVerse = m[0] + replacement + m[1]

    else:
        collector = []
        idx = random.randint( 0, parts - 1 )
    # FIXME: start here
    #    for i in range( parts - 1 ):
    #        if i == idx:

    return processedVerse
        
def generateAnagramText( vt, r ):
    m = re.search( 'the master', vt, re.IGNORECASE )
    if m:
        idx = random.randint( 0, len( r['verseText']['theMaster'] ) - 1 )
        replacement = r['verseText']['theMaster'][ idx ]
        replaceMaster( vt, replacement )
        return 'the master'

    for p in r['verseText']['computed']:
        m = re.search( p, vt, re.IGNORECASE )
        if m:
            return p

    return 'unmatched'

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

f = open( 'replacements.yaml' )
replacements = yaml.load( f )
f.close()
random.shuffle( replacements['verseText']['theMaster'] )

f = open( 'raw-analects.yaml' )
analects = yaml.load( f )
f.close()

for book in analects:
    for chapter in book['bookChapters']:
        for verse in chapter['chapterVerses']:
            anagramText = generateAnagramText( verse['verseText'], replacements )
            print anagramText

# add 'anagramText' key to verse object
# add 'info' key with date/time of replacement
## also maybe other interesting stats
# dump updated data to yaml


