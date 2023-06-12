import os
import re
import time 
import random as rand


textDir = "./text/"
testDir = "./test/"

class WordNode:
    def __init__(self, word="") -> None:
        self.children = []
        self.word = word
        self.weight = 1
    
    def getNextWord(self):
        return getStrongestWord(self.children)

    def __str__(self) -> str:
        return f"{self.word} {self.weight}"


def getStrongestWord(wordNodeList):
    next = WordNode()
    next.weight = -1
    for n in wordNodeList:
        if n.weight > next.weight:
            next = n
    return next

def getRandomWord(wordNodeList):
    if len(wordNodeList) > 0:
        index = rand.randint(0, len(wordNodeList) - 1)
        return wordNodeList[index]
    else:
        return WordNode()

def wordsBeforeAfter(words, index):
    if len(words) <= 1 or (index < 0 and index >= len(words)):
        return "", ""
    isFirst = index == 0
    isLast = index == len(words) - 1
    if isFirst:
        return "", words[index + 1]
    elif isLast:
        return words[index - 1], ""
    else:
        return words[index - 1], words[index + 1]
    
    

def isInt(val):
    try:
        return type(int(val)) is int
    except:
        return False 
def readFiles(directory):
    if os.path.exists(directory) and os.path.isdir(directory):
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                for line in file.readlines():
                    yield line

def wordList(sentence):
    # Split sentence into words without punctuation.
    line = re.sub("[^a-zA-Z ]", "", sentence).strip().lower()
    return line.split(" ")

def createWordMap():
    wordMap = {}
    for line in readFiles(textDir):
        # Match verses, which have a number at the start.
        if isInt(line.split(" ")[0]):
            words = wordList(line)
            for i in range(0, len(words)):
                w = words[i]
                prev, next = wordsBeforeAfter(words, i)
                # Create map where a string key corresponds to a list of word nodes.
                addWordToMap(wordMap, w, next)
    return wordMap

def addWordToMap(wordMap, word, nextWord):
    # Add word to the map along with another word that will follow it in a sentence.
    if not word in wordMap.keys():
        wordMap[word] = [ WordNode(nextWord) ]
    else:
        added = False
        for n in wordMap[word]:
            if n.word == nextWord:
                n.weight += 1
                added = True
                break
        if not added:
            wordMap[word].append(WordNode(nextWord))

print("Loading...")
wmap = createWordMap()
print("Finished. Enter a word & I will try to guess the next..")


learningEnabled = True
word = ""
lastGuess = ""
while word != "q":
    word = re.sub("[^a-zA-Z]", "", input("?").lower().strip())

    # Add the user's response to my last guess as a new option.
    if learningEnabled and lastGuess != "" and word != "":
        addWordToMap(wmap, lastGuess, word)

    lastGuess = getRandomWord(wmap[word]) if word in wmap.keys() else ""
    print(lastGuess)

