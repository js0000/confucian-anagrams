# add-anagrams.py
# adds "anagram processed" texts to python data structure

import random
import re
import yaml

## DEBUG
#import pprint
#pp = pprint.PrettyPrinter( indent = 2 )

## GLOBALS
masterCounter = 0


## SUBROUTINES
def replaceMaster( vt, replacement ):
    verseList = re.split( '(the master)', vt, flags=re.IGNORECASE )
    processedVerse = False
    parts = len( verseList )
    if parts == 0:
        print( 'split fails for ' + vt )
        return False
        
    else:
        collector = []
        idx = random.randint( 0, parts / 2 )
        # needs to be modified to work with re.split return data
        # replacement will be either only odd or only even
        idx *= 2
        if not re.match( '^the master$', verseList[0], flags=re.IGNORECASE ):
            if idx > 0:
                idx -= 1
            else:
                idx += 1
        for i in range( parts ):
            if len( verseList[ i ] ) < 1:
                continue

            if re.match( '^the master$', verseList[ i ], flags=re.IGNORECASE ):
                if verseList[ i ].istitle():
                    if i == idx:
                        collector.append( replacement.title() ) 
                    else:
                        collector.append( 'The Master' )
                else:
                    if i == idx:
                        collector.append( replacement )
                    else:
                        collector.append( 'the Master' )
            else:
                collector.append( verseList[ i ] )

    return ''.join( collector )
       
        
# arg b is boolean
# determining whether to cycle through options
# not implemented
def selectMasterReplacement( r, b ):
    global masterCounter
    if b:
        replacement = r['verseText']['theMaster'][ masterCounter ]
        i = masterCounter + 1
        moduloBase = len( r['verseText']['theMaster'] )
        masterCounter = i % moduloBase
    else:
        random.shuffle( replacements['verseText']['theMaster'] )
        idx = random.randint( 0, len( r['verseText']['theMaster'] ) - 1 )
        replacement = r['verseText']['theMaster'][ idx ]

    return replacement


def generateAnagramText( vt, r ):
    m = re.search( 'the master', vt, flags=re.IGNORECASE )
    if m:
        replacement = selectMasterReplacement( r, False )
        anagramVerse = replaceMaster( vt, replacement )
        return anagramVerse

    for p in r['verseText']['computed']:
        m = re.search( p, vt, flags=re.IGNORECASE )
        if m:
            # FIXME: this is the curl replacement
            return 'c'

    # FIXME: this is the random text replacement
    return 'x'

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

f = open( 'raw-analects.yaml' )
analects = yaml.load( f )
f.close()

for book in analects:
    for chapter in book['bookChapters']:
        for verse in chapter['chapterVerses']:
            anagramText = generateAnagramText( verse['verseText'], replacements )

# add 'anagramText' key to verse object
# add 'info' key with date/time of replacement
## also maybe other interesting stats
# dump updated data to yaml
