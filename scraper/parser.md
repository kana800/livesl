<h3 align="center">Parser</h3>

### Parser Output with `Normal Post` and `Live Post`

```
scraper\scrapeddata\thesoulsrilanka\latest.jpg [Well well well....look who's …] json

------------------------POST---------------------------

Well well well....look who's back old friend....@dotsbayhouse

 7 years of supporting original music and wishing them plenty more.

 We're playing there again on the
 1st of December 2022.

 THURSDAY! Come for the weekend!

 Entry - LKR 2000

 Tickets at the gatee!!!

 Let the season and celebrations begin.

 Hiri babe hear we come.

 #thesoulsrilanka #dotsbayhouse #7thanniversary #livemusicvenue #originalmusic #supportoriginalmusic #srilanka #srilankatourism #tourism #matara #hiriketiya #dickwella #talalla #tangalle #weligama #madiha #boomlive


------------------------POST---------------------------

-->Detected As Live Event<--



Hash Tag Score: (3, 16)
Common Word Score: (3, 10)
NER Score: (2, 5)
---------------------------------

live event ->  True
---------------------------------


[A clip from our @thattu.pattu…] json

------------------------POST---------------------------

A clip from our @thattu.pattu live performance video

 You can watch the full video on the Thattu Pattu Website - the link is in our bio!
 .
 .
 .
 #alternativemusic
 #singersongwriter #livemusic #indiepop #singer #songwriter #smusic #art #experimentalmusic #performancevideo #alternativestyle #owltreeo #owlsessions #thattupattu


------------------------POST---------------------------

-->Not Detected As Live Event<--



Hash Tag Score: (1, 14)
Common Word Score: (0, 10)
NER Score: (0, 1)
---------------------------------

live event ->  False
```


### Table Of Content

- `scrapeddata/*`: scraped data
- `pytest/parsertest.py`: test cases for the parser

This document explains how exactly the parser works. After a post is scraped we need to identify whether the given post has a "possibility" of being a **post about a live-event**. 

We will be scoring the posts according to several key points and we will be using [`spacy`](https://spacy.io/). 

---

The detection part of the algorithm is very *hacky*. It just look at only certain keywords. Since I am doing it in a rush I am not going to implement this properly maybe in the future I will :pray:

The section below gives a small description on how the *detection* algorithm works.

---

<p style="text-align: center" align="center">
  <img src="https://github.com/opensrilanka/livesl/blob/main/scraper/.images/parserflow.png" alt="parser algorithm">
  <p align="center">
	Quick overview of the Parser algorithm.
  </p>
</p>

#### Hashtags `#hashtags`

Normally each post consist of several `hashtags`; First task to *separate* the `hashtags` from the post and will be *searching* for specific `hashtags` like:

```
#liveevent #livemusic #srilanka #livemusicvenue
```

> **1 point will be given for each *successful* match**

#### Words, Nouns and Verbs

After that we will be *searching* for the *most-common words* in the post; These words will include:
- verbs
- nouns

Normally post with *live-events* consist of 

- *verbs*: 
```
playing supporting coming
```

- *nouns*:
```
gig entry music
```

> **1 point will be given for each *successful* match**

#### Named Entity Recognition

After that we will try to find **named entity** in the `description`. We will be looking for stuff like :

- Dates
- Organization
- Currencies/Prices
- Time
- Location

> **1 point will be given for each *successful* match**

---

#### Identifying Dates

There are several possible methods the post will mention dates:

- `5th december 2022` : `2022 | DATE | Absolute or relative dates or periods`
- `5thdecember 2022`: `5thdecember2022 | CARDINAL | Numerals that do not fall under another type`
- `05/12/2022`: `05/12/2022 | CARDINAL | Numerals that do not fall under another type`
- `12/05/2022`: `12/05/2022 | DATE | Absolute or relative dates or periods`
- `2022/05/12`: `2022/05/12 | CARDINAL | Numerals that do not fall under another type`
- `2022/12/05`: `2022/12/05 | CARDINAL | Numerals that do not fall under another type`

Majority of the time `ents` of `Date` get recognized as `DATE, CARDINAL`. To detect dates in the string we will look for the `left-span-entity` and `right-span-entity`. `regex` will be used to detect date versions like `mm/dd/yyyy`. 

---

#### Identifying Location

Most of the time `locations` are *tagged* in the *post*. `@` will be used to tag a place; The next problem will be to check whether the *tagged* place is *location* or a *person*. 


#### Identifying Currency/Prices

We can use *currency* tags to identify *currency*. Tags:

```
LKR
USD
$
Rs
```
---