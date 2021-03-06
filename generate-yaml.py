# generate-yaml.py
# reads raw-analects.txt
# converts to python data structure
# dumps to file


import pprint
import re
import sys
import yaml

# ROMAN INT CONVERSION
# from http://code.activestate.com/recipes/81611-roman-numerals/


def int_to_roman(input):
    """
    Convert an integer to Roman numerals.

    Examples:
    >>> int_to_roman(0)
    Traceback (most recent call last):
    ValueError: Argument must be between 1 and 3999

    >>> int_to_roman(-1)
    Traceback (most recent call last):
    ValueError: Argument must be between 1 and 3999

    >>> int_to_roman(1.5)
    Traceback (most recent call last):
    TypeError: expected integer, got <type 'float'>

    >>> for i in range(1, 21): print int_to_roman(i)
    ...
    I
    II
    III
    IV
    V
    VI
    VII
    VIII
    IX
    X
    XI
    XII
    XIII
    XIV
    XV
    XVI
    XVII
    XVIII
    XIX
    XX
    >>> print int_to_roman(2000)
    MM
    >>> print int_to_roman(1999)
    MCMXCIX
    """
    if not isinstance(input, int):
        msg = "expected integer, got %s" % type(input)
        raise TypeError(msg)
    if not 0 < input < 4000:
        raise ValueError("Argument must be between 1 and 3999")
    ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
    nums = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL',
            'X', 'IX', 'V', 'IV', 'I')
    result = ""
    for i in range(len(ints)):
        count = int(input / ints[i])
        result += nums[i] * count
        input -= ints[i] * count
    return result


def roman_to_int(input):
    """
    Convert a roman numeral to an integer.

    >>> r = range(1, 4000)
    >>> nums = [int_to_roman(i) for i in r]
    >>> ints = [roman_to_int(n) for n in nums]
    >>> print r == ints
    1

    >>> roman_to_int('VVVIV')
    Traceback (most recent call last):
     ...
    ValueError: input is not a valid roman numeral: VVVIV
    >>> roman_to_int(1)
    Traceback (most recent call last):
     ...
    TypeError: expected string, got <type 'int'>
    >>> roman_to_int('a')
    Traceback (most recent call last):
     ...
    ValueError: input is not a valid roman numeral: A
    >>> roman_to_int('IL')
    Traceback (most recent call last):
     ...
    ValueError: input is not a valid roman numeral: IL
    """
    if not isinstance(input, str):
        msg = "expected string, got %s" % type(input)
        raise TypeError(msg)
    input = input.upper()
    nums = ['M', 'D', 'C', 'L', 'X', 'V', 'I']
    ints = [1000, 500, 100, 50,  10,  5,   1]
    places = []
    for c in input:
        if c not in nums:
            msg = "input is not a valid roman numeral: %s" % input
            raise ValueError(msg)
    for i in range(len(input)):
        c = input[i]
        value = ints[nums.index(c)]
        # If the next place holds a larger number, this value is negative.
        try:
            nextvalue = ints[nums.index(input[i + 1])]
            if nextvalue > value:
                value *= -1
        except IndexError:
            # there is no next place.
            pass
        places.append(value)
    sum = 0
    for n in places:
        sum += n
    # Easiest test for validity...
    if int_to_roman(sum) == input:
        return sum
    else:
        msg = 'input is not a valid roman numeral: %s' % input
        raise ValueError(msg)


# MAIN
def main():
    f = open('raw-analects.txt', 'r')
    pp = pprint.PrettyPrinter(indent=2)
    analects = []
    currentBook = {'bookChapters': []}
    currentChapter = {'chapterVerses': []}
    nextLineTitle = False
    for line in f:
        # skip blanks
        m = re.match('^\s*$', line)
        if m:
            continue
        l = line.rstrip()
        if nextLineTitle:
            currentBook['bookName'] = l.rstrip('.')
            nextLineTitle = False
            continue
        else:
            m = re.match('^(\d+)\. (.+)$', l)
            if m:
                verseDict = {}
                verseDict['verseNumber'] = int(m.group(1))
                verseDict['verseText'] = m.group(2)
                currentChapter['chapterVerses'].append(verseDict)
            m = re.match('^BOOK (\w+)\.', l)
            if m:
                if 'bookNumber' in currentBook:
                    # clean up old chapter
                    currentBook['bookChapters'].append(currentChapter)
                    currentChapter = {'chapterVerses': []}
                    analects.append(currentBook)
                    currentBook = {'bookChapters': []}
                r = m.group(1)
                currentBook['bookNumber'] = roman_to_int(r)
                nextLineTitle = True
                continue

            m = re.match('^CHAP\. (\w+)\.', l)
            if m:
                if 'chapterNumber' in currentChapter:
                    currentBook['bookChapters'].append(currentChapter)
                    currentChapter = {'chapterVerses': []}
                r = m.group(1)
                currentChapter['chapterNumber'] = roman_to_int(r)
                continue
    # clean up
    currentBook['bookChapters'].append(currentChapter)
    analects.append(currentBook)
    f.close()

    f = open('raw-analects.yaml', 'w')
    yaml.dump(analects, f,
              default_flow_style=False, width=9999, explicit_start=True)
    f.close()
    sys.exit()


if __name__ == '__main__':
    main()


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
#   create new anonymous currentVerse dictionary and append to CurrentChapter
