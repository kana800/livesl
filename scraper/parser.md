<h3 align="center">Parser</h3>

Other Content Related Parser
- `scrapeddata/*`: scraped data
- `pytest/parsertest.py`: test cases for the parser
- `Analysis Of Post`: Notebook containing *analysis* of instagram post made by several bands.

This document explains how exactly the parser works. After a post is scraped we need to identify whether the given post has a "possibility" of being a **post about a live-event**. 

We will be scoring the posts according to several key points and we will be using [`spacy`](https://spacy.io/) for [further analysis](AnalysisOfPost.ipynb) of the post `description`. 

checkout [Analysis Of Post](AnalysisOfPost.ipynb) for indepth detail report about the `description` about `posts`.


---

<p style="text-align: center" align="center">
  <img src="https://github.com/opensrilanka/livesl/tree/main/scraper/.images/parserflow.png" alt="parser algorithm">
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

#### Combo's & Specific Details

If `prices` are mentioned in a post there is a higher chance that the post mentioned will be related to a *live-event*.

---