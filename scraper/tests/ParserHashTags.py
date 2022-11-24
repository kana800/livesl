"""
TestCases for the ScoreHashTag Function
---------------------------------------
This file contains test cases for:
- scoreHashTags(desc)
- IsInHashTags(wrd)
- scrapeHashTags(desc)
"""
import pytest
import sys
sys.path.append('../scraper')


from scraper.parser import scrapeHashTags,\
     scoreHashTags, IsInHashTags
from tests.TestStrings import teststringdict


def test_scoreHashTags():
     for idx, [teststr, hashonlystr, score] in teststringdict.items():
          (predscore, predkeywords) = scoreHashTags(teststr)
 
          assert predscore == score
          assert predkeywords == len(hashonlystr.split(" "))

def test_isInHashTags():
     teststr = ["#liveevent", "#cake", "power", "1523"]
     #output = [1, 0 , 0 , 0]
     ansli = list(map(IsInHashTags, teststr))
     assert ansli == [1 , 0 , 0 , 0]

def test_scrapeHashTags():
     for idx, [teststr, hashonlystr, _] in teststringdict.items():
          ansli = scrapeHashTags(teststr)
          hashonlyli = hashonlystr.split(" ")
          
          assert len(ansli) == len(hashonlyli)

          # checking if hashes are present in the
          # hash only list
          for hashes in ansli:
               assert hashes in hashonlyli