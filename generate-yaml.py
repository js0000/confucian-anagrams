# generate-yaml.py
# reads raw-analects.txt
# creates YAML output

f = open( 'raw-analects.txt', 'r' )

analects = []
currentBook = {}
currentChapter = {}

nextLineProcessing = False
for line in f:
    print line

# PARSING LOGIC

# if nextLineProcessing
#   follow directions

# if ^BOOK (number).
#   if currentBook has keys, append to analects list
#   create new currentBook dictionary
#   set nextlineProcessing to 'book name'

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
