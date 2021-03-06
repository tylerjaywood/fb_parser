import nltk
from bs4 import BeautifulSoup as bs

stubfile = "/Users/tylerw/msgsample.htm"
fullfile = "/Users/tylerw/Downloads/facebook-tylerjaywoodd/html/messages.htm"

def tokenizeString(string):
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w{4,}')
    tokenized = tokenizer.tokenize(string)
    return tokenized

def removeStopWords(wordlist):
    goWords = [word.lower() for word in wordlist if word.lower()
                not in nltk.corpus.stopwords.words('english')]
    return goWords

def prepString4Nltk(string):
    tokenized = tokenizeString(string)
    tokenized = [x.lower() for x in tokenized]
    words = removeStopWords(tokenized)
    return words

class Thread(object):
    def __init__(self, threadSoup):
        self.soup = threadSoup
        self.participants = [name.strip() for name in
                        threadSoup.contents[0].split(',')]
        self.messagesSoup = self.soup.findAll('div', {"class":"message"})
        self.Messages = True

    def aggregateMessages(self):
        self.Messages = [Message(msg) for msg in self.messagesSoup
                                if len(msg.findNext('p').contents) > 0]

class Message(object):
    def __init__(self, msgSoup):
        self.sender = msgSoup.find('span').contents[0]
        self.content = msgSoup.findNext('p').contents[0]
        self.meta = msgSoup.find('span', {"class":"meta"})

    def printMessage(self):
        print(self.content)

class Archive(object):
    def __init__(self, filepath):
        self.archivePath = filepath
        self.makeArchiveSoup()
        self.pullThreads()

    def makeArchiveSoup(self):
        with file(self.archivePath) as f:
            raw = f.read()
            self.archiveSoup = bs(raw)
        print "archive is souped"

    def personInConvo(self, name, threadObj):
        if name in threadObj.participants:
            return True
        else:
            return False

    def pullThreads(self):
        self.threadObjects = [Thread(x) for x in
                self.archiveSoup.findAll("div", {"class" : "thread"})]
        print "threads are pulled"

    def pullMessages(self):
            [thread.aggregateMessages() for thread in self.threadObjects]

    def personThreads(self, *members):
        """For all names provided in members, extract threads in which
        they are participants and return a dict of
        {Person: [Thread objects]}"""

        memList = [name for name in members]
        personThreadDict = {name: [] for name in memList}
        memList = [name for name in members]
        for thread in self.threadObjects:
            for name in memList:
                if self.personInConvo(name, thread):
                    personThreadDict[name].append(thread)
                else:
                    pass
        return personThreadDict

    def personMessages(self, *members):
        """For all names provided in members, create personThreadDict
        and then iterate through the dict to collect all string messages
        sent by provided people. Return a dict of:
        {Person: ["lorem ipsum etc..."]"""

        memList = [name for name in members]
        personMessageDict = {name:"" for name in memList}
        personThreadDict = self.personThreads(*members)
        for threadcollection in personThreadDict.itervalues():
            for thread in threadcollection:
                thread.aggregateMessages()
                for message in thread.Messages:
                    if message.sender in memList:
                        name = message.sender
                        personMessageDict[name] += ("\n" + message.content)
        return personMessageDict

class PeopleArchive(Archive):
    def __init__(self,  *members):
        # super(PeopleArchive, self).__init__(filepath)
        self.members = [name for name in members]
        self.archiveSoup = bar.archiveSoup
        self.threadObjects = bar.threadObjects
        self.probList = {}

    def pullPersonMessages(self):
        """
        Finds threads with all of members
        returns a dict of {member: "all their text"}
        """
        personMessageDict = {name: "" for name in self.members}
        test = []
        for thread in self.threadObjects:
            if len(set(self.members) & set(thread.participants)) > 0:
                test.append(thread.participants)
                thread.aggregateMessages()
                for message in thread.Messages:
                    if message.sender in self.members:
                        name = message.sender
                        personMessageDict[name] += ("\n" + message.content)
            else:
                pass
        self.personMessageDict = personMessageDict

    def prepPersonMessageDict(self, *people):
        for person in people:
            if person in self.personMessageDict.keys():
                self.personMessageDict[person] = \
                        prepString4Nltk(self.personMessageDict[person])


    def findTopWords(self, *person):
        pass

    def assignProbabilities(self, person):
        fd = nltk.FreqDist(self.personMessageDict[person])
        probDist = nltk.MLEProbDist(fd)
        for y in probDist.samples():
            self.probList[y] =  probDist.prob(y)


def checkPersonUniqueWords(person, peopleDict):
    personDict = peopleDict[person]
    returnVec = []
    for word in personDict:
        unique = True
        for name in peopleDict:
            try:
                if peopleDict[name][word] > personDict[word]:
                    unique = False
                else:
                    pass
            except KeyError:
                pass
        if unique == True:
            returnVec.append((word, personDict[word]))
    return returnVec

if __name__ == "__main__":
    bar = Archive(stubfile)

#    agg = {}
#
#    for thread in bar.threadObjects:
#        for person in thread.participants:
#            print person
#            if person not in agg:
#                agg[person] = PeopleArchive(person)
#            else:
#                continue
#
#    print len(agg)
#
#    probListDict = {}
#
#    for x, v in agg.items():
#        print "pulling messages " + x
#        #agg[x].pullMessages
#        agg[x].pullPersonMessages()
#
#        agg[x].prepPersonMessageDict(x)
#        print "probs for " + x
#        agg[x].assignProbabilities(x)
#        probListDict[x] = agg[x].probList
#
#
#    print "jason"
#    print "\n"
#    e = checkPersonUniqueWords('Aparna Nemana', probListDict)
#    es = sorted(e, key = lambda x: x[1])
#
#    for x in es[-50:]:
#        print x[0],"\t", x[1]
