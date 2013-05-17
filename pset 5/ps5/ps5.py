# 6.00 Problem Set 5
# RSS Feed Filter

#name: Moe Amaya
#collaborators: none
#time: 10:00

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

class NewsStory(object):
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers

class WordTrigger(Trigger):
    def evaluate(self, story):
        raise NotImplementedError
    
    def is_word_in(self, story):
        lower = story.lower()
        
        sep = string.punctuation
        newString = lower
        
        for char in sep:
            newString = newString.replace(char, " ")
    
        return newString.split()


class TitleTrigger(WordTrigger):
    def __init__(self, text):
        self.text = text.lower()

    def evaluate(self, story):
        title = story.get_title()

        wt = WordTrigger()
        titleWords = wt.is_word_in(title)
        
        if self.text in titleWords:
            return True
        else:
            return False


class SubjectTrigger(WordTrigger):
    def __init__(self, text):
        self.text = text.lower()

    def evaluate(self, story):
        subject = story.get_subject()

        wt = WordTrigger()
        subjectWords = wt.is_word_in(subject)

        if self.text in subjectWords:
            return True
        else:
            return False
        

class SummaryTrigger(WordTrigger):
    def __init__(self, text):
        self.text = text.lower()

    def evaluate(self, story):
        summary = story.get_summary()

        wt = WordTrigger()
        summaryWords = wt.is_word_in(summary)

        if self.text in summaryWords:
            return True
        else:
            return False


# Composite Triggers

class NotTrigger(Trigger):
    def __init__(self, word):
        self.word = word

    def evaluate(self, story):
        if not self.word.evaluate(story):
            return True
        else:
            return False

class AndTrigger(Trigger):
    def __init__(self, word1, word2):
        self.word1 = word1
        self.word2 = word2

    def evaluate(self, story):
        test1 = self.word1
        test2 = self.word2

        if test1.evaluate(story) and test2.evaluate(story):
            return True
        else:
            return False
        
class OrTrigger(Trigger):
    def __init__(self, word1, word2):
        self.word1 = word1
        self.word2 = word2

    def evaluate(self, story):
        test1 = self.word1
        test2 = self.word2

        if test1.evaluate(story) or test2.evaluate(story):
            return True
        else:
            return False


# Phrase Trigger

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, story):
        self.list = [story.get_guid(), story.get_title(), story.get_subject(), story.get_summary(), story.get_link()]
        for category in self.list:
            if self.phrase in category:
                return True
        return False
                     
#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    listStories = []
    
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                listStories.append(story)
           
    return listStories
    
#======================
# Part 4
# User-Specified Triggers
#======================

def makeTrigger(trigger_map, trigger_type, params, name):
    """
    Takes in a map of names to trigger instance, the type of trigger to make,
    and the list of parameters to the constructor, and adds a new trigger
    to the trigger map dictionary.

    trigger_map: dictionary with names as keys (strings) and triggers as values
    trigger_type: string indicating the type of trigger to make (ex: "TITLE")
    params: list of strings with the inputs to the trigger constructor (ex: ["world"])
    name: a string representing the name of the new trigger (ex: "t1")

    Modifies trigger_map, adding a new key-value pair for this trigger.

    Returns: None
    """
    
    pass

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all_lines = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all_lines:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

# ---------------------------
# Didn't have time to finish
#----------------------------


##    for trigger in lines:
##        parseTrig = trigger.split()
##
##        if parseTrig[0] != "ADD":
##            if parseTrig[1] == "TITLE":
##                
##            elif parseTrig[1] == "SUBJECT":
##                pass
##            elif parseTrig[1] == "SUMMARY":
##                pass
##            elif parseTrig[1] == "NOT":
##                pass
##            elif parseTrig[1] == "AND":
##                pass
##            elif parseTrig[1] == "OR":
##                pass
##            elif parseTrig[1] == "PHRASE":
##                pass
##        else:
##            pass
            

 #       makeTrigger(trigger_map, trigger_type, params, name)
    
import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    t1 = TitleTrigger("Syria")
    t2 = SubjectTrigger("Iran")
    t3 = PhraseTrigger("Wall Street")
    t4 = OrTrigger(t2, t3)
    triggerlist = [t1, t4]
    

 #   triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print "Polling . . .",

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            print ". . .",
            if story.get_guid() not in guidShown:
                newstories.append(story)
        print ". . ."
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

