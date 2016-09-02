# add-anagrams.py
# adds "anagram processed" texts to python data structure

import random
import re
import yaml

## DEBUG
#import pprint
#pp = pprint.PrettyPrinter( indent = 2 )


## SUBROUTINES
def replaceMaster( vt, replacement ):
    m = re.split( 'the master', vt, flags=re.IGNORECASE )
    processedVerse = False
    parts = len( m )
    if parts == 0:
        print( 'split fails for ' + vt )
        return False
        
    elif parts == 2:
        if len( m[0] ) == 0:
            processedVerse = replacement + m[1]
        elif len( m[1] ) == 0:
            processedVerse = m[0] + replacement
        else:
            processedVerse = m[0] + replacement + m[1]

    else:
        # FIXME: not quite sure this is working if idx == parts - 1
        collector = []
        idx = random.randint( 0, parts - 1 )

        if idx == 0 and len( m[0] ) == 0:
            collector.append( replacement )
            collector.append( m[1] );
            for i in range( 2, parts ):
                collector.append( 'the Master' )
                collector.append( m[ i ] );
        else:
            if len( m[0] ) == 0:
                collector.append( 'The Master' )

            for i in range( parts - 1 ):
                collector.append( m[ i ] )
                if i == idx:
                    collector.append( replacement )
                else:
                    collector.append( 'the Master' )

            if len( m[ parts - 1 ] ) == 0 and idx == ( parts - 1 ):
                collector.append( replacement )
            elif len( m[ parts - 1 ] ) == 0:
                collector.append( 'the Master' )
            else:
                collector.append( m[ parts - 1 ] )
        processedVerse = ''.join( collector )

    return processedVerse
        
def generateAnagramText( vt, r ):
    m = re.search( 'the master', vt, flags=re.IGNORECASE )
    if m:
        # FIXME: should have option to cycle through replacements
        idx = random.randint( 0, len( r['verseText']['theMaster'] ) - 1 )
        replacement = r['verseText']['theMaster'][ idx ]
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
random.shuffle( replacements['verseText']['theMaster'] )

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
