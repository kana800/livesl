"""
TestCases for the ScoreHashTag Function
---------------------------------------
This file contains test cases for:
- scoreHashTags(desc)
- IsInHashTags(wrd)
- scrapeHashTags(desc)
"""
import spacy 

# loading spacy
nlp = spacy.load("en_core_web_sm")