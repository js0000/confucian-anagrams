# add-anagrams.py
# adds "anagram processed" texts to python data structure

import random
import re
import sys
import yaml

# DEBUG
import pprint
pp = pprint.PrettyPrinter(indent=2)

# GLOBALS
masterCounter = 0


# SUBROUTINES

# FIXME: code needs to be written
# select anagram text by looking for long words
# continue as if found long word was computed list string
# and further lengthen as necessary
def randomTextReplacement(vt):
    """Replaces arbitrary text within verse, tries to process text containing
    longest words within verse."""
    anagramVerse = '!!! random text replacement not written: '
    anagramVerse += vt
    return anagramVerse


# FIXME: investigate case
# where split occurs with punctuation immediately after stub
#   find string in text and add words on each side until > N length
#   do not cross punctuation boundaries
#   shuffle anagram words and replace
def replaceStub(vt, s):
    """Given a verse and a stub, creates a longer excerpt from the verse
    featuring the stub and replaces it with an anagram thereof."""

    # split on stub
    verseList = re.split(s, vt, flags=re.IGNORECASE)
    parts = len(verseList)
    beforeStub = []
    afterStub = []

    # no matches
    if parts == 0:
        msg = ' '.join(['split on',
            s,
            'fails [verseText]:',
            vt])
        raise ValueError(msg)
    # multiple matches
    elif parts > 2:
        # determine where split will take place
        splitIdx = random.randint(0, parts - 2)
        for i in range(parts):
            if i < splitIdx:
                wordList = re.split('\s+', verseList[i])
                for j in range(len(wordList)):
                    if j == 0 and len(beforeStub) < 1:
                        beforeStub.append(wordList[j])
                    else:
                        beforeStub.append(wordList[j])
                # remove empty string from end
                lastIdx = len(beforeStub) - 1
                if beforeStub[lastIdx] == '':
                    del beforeStub[lastIdx]
                beforeStub.append(s)
            elif i == splitIdx:
                wordList = re.split('\s+', verseList[i])
                for j in range(len(wordList)):
                    beforeStub.append(wordList[j])
            else:
                wordList = re.split('\s+', verseList[i])
                for j in range(len(wordList)):
                    if j == 0 and len(afterStub) < 1:
                        afterStub.append(wordList[j])
                    elif j == 0:
                        pass
                    else:
                        afterStub.append(wordList[j])
                lastIdx = len(afterStub) - 1
                if afterStub[lastIdx] == '':
                    del afterStub[lastIdx]
                afterStub.append(s)
        # remove extra stub at end
        lastIdx = len(afterStub) - 1
        del afterStub[lastIdx]
    else:
        beforeStub = re.split('\s+', verseList[0])
        afterStub = re.split('\s+', verseList[1])

    # DEBUG
    print('parts: ' + str(parts))
    print('beforeStub')
    pp.pprint(beforeStub)
    print('stub: ' + s)
    print('afterStub')
    pp.pprint(afterStub)
    print("\n")

    return True


def replaceMaster(vt, replacement):
    verseList = re.split('(the master)', vt, flags=re.IGNORECASE)
    processedVerse = False
    parts = len(verseList)

    # no matches
    if parts == 0:
        print('split fails for ' + vt)
        return False
    else:
        collector = []
        idx = random.randint(0, parts / 2)
        # needs to be modified to work with re.split return data
        # replacement will be either only odd or only even
        idx *= 2
        if not re.match('^the master$', verseList[0], flags=re.IGNORECASE):
            if idx > 0:
                idx -= 1
            else:
                idx += 1
        for i in range(parts):
            if len(verseList[i]) < 1:
                continue

            if re.match('^the master$', verseList[i], flags=re.IGNORECASE):
                if verseList[i].istitle():
                    if i == idx:
                        collector.append(replacement.title())
                    else:
                        collector.append('The Master')
                else:
                    if i == idx:
                        collector.append(replacement)
                    else:
                        collector.append('the Master')
            else:
                collector.append(verseList[i])

    return ''.join(collector)


# arg b is boolean
# determining whether to cycle through options
def selectMasterReplacement(r, b):
    global masterCounter
    if b:
        replacement = r['replacementTexts']['theMaster'][masterCounter]
        i = masterCounter + 1
        moduloBase = len(r['replacementTexts']['theMaster'])
        masterCounter = i % moduloBase
    else:
        random.shuffle(meta['replacementTexts']['theMaster'])
        idx = random.randint(0, len(r['replacementTexts']['theMaster']) - 1)
        replacement = r['replacementTexts']['theMaster'][idx]

    return replacement


def generateAnagramText(vt, r):
    """Examines input verse text to determine how it should be processed. There
    are three paths for processing:
    1. text contains 'the master'
    2. text contains one of the replacement stubs
    3. text does not contain any hints for processing
    Each verse is passed through these steps until a match is found."""

    anagramVerse = False
    m = re.search('the master', vt, flags=re.IGNORECASE)
    if m:
        replacement = selectMasterReplacement(r, False)
        anagramVerse = replaceMaster(vt, replacement)
    else:
        for s in r['replacementTexts']['stubs']:
            m = re.search(s, vt, flags=re.IGNORECASE)
            if m:
                anagramVerse = replaceStub(vt, s)
        if not anagramVerse:
            anagramVerse = randomTextReplacement(vt)
    return anagramVerse

# process each verseText using regex
# in case of multiple matches in a string, choose only one to replace
#  if 'the Master' exists directly replace
#  else
# if original text has initial uppercase letter, do the same for replacement


# MAIN
# FIXME
# - add 'anagramText' key to verse object
# - add 'info' key with date/time of replacement
#   also maybe other interesting stats
# - dump updated data to yaml
def main():
    """Top level loop for processing. Opens analects source file and loops
    through each verse to generate an anagram within."""
    f = open('meta.yaml')
    meta = yaml.load(f)
    f.close()

    f = open('raw-analects.yaml')
    analects = yaml.load(f)
    f.close()

    for book in analects:
        for chapter in book['bookChapters']:
            for verse in chapter['chapterVerses']:
                anagramText = generateAnagramText(verse['verseText'], meta)
    sys.exit()

if __name__ == '__main__':
    main()

