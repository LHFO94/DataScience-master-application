#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was written for my application to the Data Science Msc at the Uva.
It takes a text file provided and processes them into a dictionary structure 
of which the key is a word from the text and its value a linked list that shows
the orrurances of the same word in other articles. It finally plots the values
to show the distribution of word frequencies. 
"""

import re
from nltk.stem import SnowballStemmer
from collections import Counter
import matplotlib.pyplot as plt


class Node:
    """Simple node class, used by LinkedList to create a node
    
    Attributes:
        article: An integer representing which article number node came from
        count: An integer representing the occurance of word
        next: Attribute used to link note togeter 
    """
    def __init__(self, article, count):
        self.article = article
        self.count = count
        self.next = None
        
    def __repr__(self):
        """This function is called by LinkedList.display() to print results"""
        if self.next != None:
            return (f"[{self.article},{self.count}] -> ")
        else:
            return (f"[{self.article},{self.count}]")


class LinkedList:
    """LinkedList class, used to pass into dictionary values
    
    Attributes:
        head: Bool Used by .insert to indicate beginning of a linked list
        article: An integer representing which article number node came from
        next: Attribute used to link note togeter
        count: An integer representing the occurance of word    
    """
    def __init__(self, article, count, head=None):
        self.head = None
        self.article = article
        self.count = count

    #Function to add a new node
    def insert(self, article, count):
        """Used to insert new Nodes into a linked list object"""
        new_node = Node(article, count)
        if self.head is None:
            self.head = new_node
            return       
        latest = self.head        
        while latest.next is not None:
            latest = latest.next            
        latest.next = new_node

    # Print the linked list
    def display(self):
        """Function for printing out results"""
        printval = self.head    
        while printval.next is not None:
            print (printval.__repr__(), end="")
            printval = printval.next
        else:
            print (printval.__repr__())

         
class Articles:
    """Class used to pre-process the provided text into separate articles and 
    words
    
    Attributes:
        text: A .txt file turned into a str
    """
    def ___init___(self, text=None):
        self.text = text
        
    def split(text):
        """Splits the text into seperate articles"""
        articles = re.split("<doc>", text)
        del articles[0]
        return articles
    
    def get_lenght(text):
        """Used to ceate the words container"""
        return range(len(Articles.split(text)))
    
    #Cleaning the articles and extracting words     
    def pre_process(articles, stemmer, words):  
        """Cleans the articles and split them into separate words"""
        for i in range(len(articles)):
            #Removes all <...> and </...> patterns
            articles[i] = re.sub("<\w{0,8}\>", '', articles[i])
            articles[i] = re.sub("</\w{0,8}\>", '' , articles[i])
            #Removes all the \n patterns
            articles[i] = re.sub(r'\n', r'', articles[i])
            #Removes all the la... patterns
            articles[i] = re.sub(r'\w\w\d{6}\W\d{4}', r'', articles[i])
            #Removes all non-aplha/numeric characters except spaces
            articles[i] = re.sub(r'([^\s\w]|_)+', '', articles[i])
            #Removes all numbers
            articles[i] = re.sub(r'\d+', '', articles[i])
            #Removes all capital letters
            articles[i] = articles[i].lower()
            #Extracting the words from the text
            word = re.split(' ', articles[i])
            for word in word:
                #Stemming the words using the Snowball algorithm from NLTK library
                word = stemmer.stem(word)
                #Put the words in a temp storage, remembering article number
                words[i].append(word)


def create_linkedlist(words, dic): 
    """Creates a linked list with a header node and links other nodes"""
    #Loop over articles     
    for i in range(len(words)):
        #Counts the occurances of word per article
        words[i] = Counter(words[i])
        #Article number counter
        article = i + 1
        for word in words[i]:
            if word not in dic:
                #Create new linkedlist
                dic[word] = LinkedList(words[i][word], article)
                #Append node to linkedlist
                dic[word].insert(article, words[i][word])
            else:
                #Append node to existing linkedlist
                dic[word].insert(article, words[i][word])
            #Print formatting
            print(f'{word} :', end="")
            dic[word].display()


def plot(words):
    """Plotting function"""
    #Create empty container to keep track of occurances per value
    occurances = {}
    #Loop over articles
    for i in range(len(words)):
        #Counts occurances per word per article
        words[i] = Counter(words[i]).values()
        #Counts the total occurance of every value
        for occurance in words[i]:
            if occurance not in occurances:
                occurances[occurance] = 1
            else:
                occurances[occurance] += 1
    #Used for plotting
    x = occurances.keys()
    y = occurances.values()
    plt.figure(figsize=(10,6))
    plt.bar(x, y)
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Distribution word frequency')
    plt.show()            


def main():                 
    #Open LA-Times articles
    f = open("txt-for-assignment-data-science.txt", "r")
    #Split the text file into seprate articles
    text = f.read()
    #CLose LA-Times articles
    f.close()
    #Creating a container for the words
    dic = {}
    #Creating a list of all words
    words = [[] * i for i in Articles.get_lenght(text)]
    #Setting the language for the stemming algorithm
    stemmer = SnowballStemmer("english")
    #Split text into separate articles
    articles = Articles.split(text)
    #extract words per article
    Articles.pre_process(articles, stemmer, words)
    #Create a linkedlist & print results
    create_linkedlist(words, dic)
    #Plot distribution graph
    plot(words)


if __name__ == "__main__":
    main()    