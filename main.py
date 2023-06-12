import os
import re
import time 
import random as rand


textDir = "./text/"
testDir = "./test/"

class WordNode:
    def __init__(self, word="", children=[]) -> None:
        self.children = children
        self.word = word
        self.weight = 1
    
    def getStrongestChildWord(self):
        next = WordNode()
        next.weight = -1
        for n in self.children:
            if n.weight > next.weight:
                next = n
        return next
    
    def getRandomChildWord(self):
        if len(self.children) > 0:
            index = rand.randint(0, len(self.children) - 1)
            return self.children[index]
        else:
            return WordNode()

    def __str__(self) -> str:
        return f"{self.word} {self.weight}"

class WordModel:
    TEXT_DIR = "./test/"
    
    def __init__(self) -> None:
        self.wordMap = {}
        self.load()

    def load(self) -> None:
        self._createWordMap(self._readFiles(self.TEXT_DIR))

    def _readFiles(self, directory: str):
        if os.path.exists(directory) and os.path.isdir(directory):
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                with open(filepath, "r", encoding="utf-8") as file:
                    for line in file.readlines():
                        yield line

    def _wordList(self, sentence: str) -> list:
        # Split sentence into words without punctuation.
        line = re.sub("[^a-zA-Z ]", "", sentence).strip().lower()
        return line.split(" ")

    def _createWordMap(self, listOfSentences: list) -> None:
        for line in listOfSentences:
            # Match verses, which have a number at the start.
            if isInt(line.split(" ")[0]):
                words = self._wordList(line)
                for i in range(0, len(words)):
                    w = words[i]
                    prev, next = wordsBeforeAfter(words, i)
                    # Create map where a string key corresponds to a list of word nodes.
                    self.addWord(w, next)

    def addWord(self, word: str, nextWord: str) -> None:
        # Add word to the map along with another word that will follow it in a sentence.
        if not word in self.wordMap.keys():
            newWord = WordNode(word, [ WordNode(nextWord) ])
            self.wordMap[word] = newWord
        else:
            added = False
            for n in self.wordMap[word].children:
                if n.word == nextWord:
                    n.weight += 1
                    added = True
                    break
            if not added:
                self.wordMap[word].children.append(WordNode(nextWord))
    
    def __getitem__(self, key: str) -> WordNode:
        if self.__contains__(key):
            return self.wordMap[key]
        else:
            return None
    
    def __contains__(self, key: str) -> bool:
        return key in self.wordMap.keys()
    
    def __len__(self):
        return len(self.wordMap.keys())


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


print("Loading...")
model = WordModel()
print("Finished. Enter a word & I will try to guess the next..")


learningEnabled = True
word = ""
lastGuess = ""
while word != "q":
    word = re.sub("[^a-zA-Z]", "", input("?").lower().strip())

    # Add the user's response to my last guess as a new option.
    if learningEnabled and lastGuess != "" and word != "":
        model.addWord(lastGuess, word)

    if word in model:
        lastGuess = model[word].getRandomChildWord()
    else:
        lastGuess = ""
    print(lastGuess)

