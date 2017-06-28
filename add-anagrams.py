# add-anagrams.py
# adds "anagram processed" texts to python data structure

import random
import re
import yaml

# DEBUG
import pprint
pp = pprint.PrettyPrinter(indent=2)

# GLOBALS
masterCounter = 0


# SUBROUTINES

# FIXME: investigate case
# where split occurs with punctuation immediately after stub
def replaceStub(vt, s):
    verseList = re.split(s, vt, flags=re.IGNORECASE)
    parts = len(verseList)
    beforeStub = []
    afterStub = []

    # no matches
    if parts == 0:
        print('split fails for ' + vt)
        return False
    elif parts > 2:
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
    m = re.search('the master', vt, flags=re.IGNORECASE)
    if m:
        replacement = selectMasterReplacement(r, False)
        anagramVerse = replaceMaster(vt, replacement)
        return anagramVerse

    for s in r['replacementTexts']['stubs']:
        m = re.search(s, vt, flags=re.IGNORECASE)
        if m:
            anagramVerse = replaceStub(vt, s)
            return 'c'

    # FIXME: this is the random text replacement
    return 'x'

# subroutine only a stub now
# coding logic explained below

# process each verseText using regex
# in case of multiple matches in a string, choose only one to replace
#  if 'the Master' exists directly replace
#  if one of computed list
#   find string in text and add words on each side until > N length
#   do not cross punctuation boundaries
#   shuffle anagram words and replace
#  else
#   select anagram text by looking for long words
#   continue as if found long word was computed list string
#    and further lengthen as necessary
# if original text has initial uppercase letter, do the same for replacement


# MAIN

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

# add 'anagramText' key to verse object
# add 'info' key with date/time of replacement
#  also maybe other interesting stats
# dump updated data to yaml
