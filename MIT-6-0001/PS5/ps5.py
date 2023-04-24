# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Marcos Ortiz
# Collaborators: none
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

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
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        '''

        Initializes a NewsStory object

        Parameters
        ----------
        guid : string
            A globally unique identifier for this news story.
        title : string
            The news story's headline.
        description : string
            A paragraph or so summarizing the news story.
        link : string
            A link to the website with the entire news story.
        pubdate : datetime
            The date that the news story was published.

        Returns
        -------
        None.

        '''
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        '''
        Returns
        -------
        string
            self.guid
        '''
        return self.guid

    def get_title(self):
        '''
        Returns
        -------
        string
            self.title
        '''
        return self.title

    def get_description(self):
        '''
        Returns
        -------
        string
            self.description
        '''
        return self.description

    def get_link(self):
        '''
        Returns
        -------
        string
            self.link
        '''
        return self.link

    def get_pubdate(self):
        '''
        Returns
        -------
        datetime
            self.pubdate
        '''
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        '''
        Parameters
        ----------
        trigger_phrase : str
            A phrase.

        Returns
        -------
        None.
        '''

        # Store the phrase as a list of words, all lowercase
        self.phrase = phrase.lower().split(' ')

    def is_phrase_in(self, input_text):
        # If the phrase is empty, the phrase is in the text
        # If the text is empty, then the phrase is not in the text
        if not self.phrase:
            return True
        if not input_text:
            return False

        # Store the input text as a list of words. I.e. a list of the
        # substrings that consist only of consecutive lowercase ascii
        #characters that appear in the input_text
        input_list = []
        next_word = ''
        for char in input_text.lower():
            if char in string.ascii_lowercase:
                next_word += char
            elif next_word:
                input_list.append(next_word)
                next_word = ''
        if next_word:
            input_list.append(next_word)

        # Go through the words in the text, and if the first word in
        # the phrase is encountered, check whether the following words in the
        # text also match the phrase.
        len_phrase = len(self.phrase)
        len_text = len(input_list)
        first_word = self.phrase[0]
        i = 0
        while i <= len_text - len_phrase:
            the_first_word_matches = (input_list[i] == first_word)
            the_rest_matches = (input_list[i:i+len_phrase] == self.phrase)
            if the_first_word_matches and the_rest_matches:
                return True
            i +=1
        return False

# Problem 3
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return self.is_phrase_in(story.get_title())

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, time):
        # Convert the string from the prescribed format to a datetime object
        str_to_dt = datetime.strptime(time, '%d %b %Y %H:%M:%S')
        # Set the time zone to EST
        str_to_dt = str_to_dt.replace(tzinfo=pytz.timezone("EST"))
        self.time = str_to_dt

# Problem 6
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        # Get the publish date of the story, and set it to EST
        story_date = story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
        # Return whether the story date is before the trigger time
        return  story_date < self.time

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        # Get the publish date of the story, and set it to EST
        story_date = story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
        # Return whether the story date is after the trigger time
        return  story_date > self.time

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)
# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """

    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                if story not in filtered_stories:
                    filtered_stories.append(story)
                #break
    return filtered_stories
    #return stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # Store the triggers as they appear
    trigger_list = []
    for line in lines:
            current_line = line.split(',')
            if current_line[1]=='TITLE':
                trigger_list.append(TitleTrigger(current_line[2]))
            elif current_line[1]=='DESCRIPTION':
                trigger_list.append(DescriptionTrigger(current_line[2]))
            elif current_line[1]=='AFTER':
                trigger_list.append(AfterTrigger(current_line[2]))
            elif current_line[1]=='BEFORE':
                trigger_list.append(BeforeTrigger(current_line[2]))
            elif current_line[1]=='NOT':
                trigger_list.append(NotTrigger(
                    trigger_list[int(current_line[2][1])-1],
                    trigger_list[int(current_line[3][1])-1]))
            elif current_line[1]=='AND':
                trigger_list.append(AndTrigger(
                    trigger_list[int(current_line[2][1])-1],
                    trigger_list[int(current_line[3][1])-1]))
            elif current_line[1]=='OR':
                trigger_list.append(OrTrigger(
                    trigger_list[int(current_line[2][1])-1],
                    trigger_list[int(current_line[3][1])-1]))
            # Once the ADD lune is reached, keep only those triggers
            elif current_line[0]=='ADD':
                add_list = [int(add_trigger[1]) for add_trigger in current_line[1:]]
                trigger_list = [trigger_list[i-1] for i in add_list]
    return trigger_list



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("supreme")
        t2 = DescriptionTrigger("ability")
        t3 = DescriptionTrigger("sleep")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]
        #triggerlist = [t1, t2, t3, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        # Title changes becuase the Yahoo! stories are no longer loaded
        # t = "Google & Yahoo Top News"
        t = "Google Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # This no longer functions properly as Yahoo! stories no longer
            # include discriptions
            #stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

