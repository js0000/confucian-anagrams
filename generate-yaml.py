# generate-yaml.py
# reads raw-analects.txt
# creates YAML output

import re
import yaml

## SUBROUTINES

# conversion routines from https://code.activestate.com/recipes/81611-roman-numerals/
numeral_map = tuple(zip(
    (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
    ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
))

def int_to_roman(i):
    result = []
    for integer, numeral in numeral_map:
        count = i // integer
        result.append(numeral * count)
        i -= integer * count
        return ''.join(result)

def roman_to_int(n):
    i = result = 0
    for integer, numeral in numeral_map:
        while n[i:i + len(numeral)] == numeral:
            result += integer
            i += len(numeral)
            return result

## MAIN
f = open( 'raw-analects.txt', 'r' )

analects = []
currentBook = { 'bookChapters' : [] }
currentChapter = { 'chapterVerses' : [] }
nextLineTitle = False

for line in f:
    
    # skip blanks
    m = re.match( '^\s*$', line )
    if m:
        continue

    l = line.rstrip()

    if nextLineTitle:
        currentBook['bookName'] = l.rstrip( '.' )
        nextLineTitle = False
        continue
    else:
        m = re.match( '^BOOK (\w+)\.', l )
        if m:
            size = len( currentBook )
            if size > 0:
                analects.append( currentBook )
                currentBook = { 'bookChapters' : [] }
            r = m.group( 1 )
            currentBook['bookNumber'] = roman_to_int( r )
            nextLineTitle = True
            continue

        m = re.match( '^CHAP\. (\w+)\.', l )
        if m:
            size = len( currentChapter )
            if size > 0:
                currentBook['bookChapters'].append( currentChapter )
                currentChapter = { 'chapterVerses' : [] }
            r = m.group( 1 )
            currentChapter['chapterNumber'] =  roman_to_int( r )
            continue

        m = re.match( '^\d+\. (.+)$', l )
        if m:
            currentChapter['chapterVerses'].append( m.group( 1 ) )

# last book onto analects
analects.append( currentBook )
f.close()

f = open( 'raw-analects.yaml', 'w' )
yaml.dump( analects, f )
f.close()


# PARSING LOGIC

# if nextLineTitle
#   follow directions

# if ^BOOK (number).
#   if currentBook has keys, append to analects list
#   create new currentBook dictionary
#   set nextlineTitle to True

# if ^CHAP. (number).
#   if currentChapter has keys, append to CurrentBook list
#   create new currentChapter dictionary

# if ^(\d+). (\w+)
#   create new anonymous currentVerse dictionary and append to last CurrentChapter

# DATA MODEL
# analects = [
#   {
#     bookName = '',
#     bookNumber = N,
#     bookChapters = [
#       {
#         chapterNumber = N,
#         chapterVerses = [
#           {
#             verseNumber = N,
#             verseText = ''
#           },
#           ...
#         ]
#       },
#       ...
#    ]
#   },
#   ...
# ]

