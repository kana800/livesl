"""
TestCases for the ScoreNamedEntities &
Other Functions Related with Spacy
---------------------------------------
This file contains test cases for:
- getNamedEntities(doc)
"""
import sys
import pytest
sys.path.append('../scraper')

import spacy 
from tests.TestStrings import testDatesString, teststringdict

from scraper.parser import detectCardinalType,\
    scoreNamedEntities, removeHashTags, IsLiveEvent

# loading spacy
nlp = spacy.load("en_core_web_sm")

def test_IsLiveEvent():
    for [string, _ , _] in teststringdict.values():
        IsLiveEvent(string)

def test_scoreNamedEntities():
    for [string, _ , _] in teststringdict.values():
        doc = nlp(string)
        for span in doc.ents:
            scoreNamedEntities(span)

def test_detectCardinalType():
    for [string, _ , _] in teststringdict.values():
        string = removeHashTags(string)
        doc = nlp(string)
        for span in doc.ents:
            detectCardinalType(span)
