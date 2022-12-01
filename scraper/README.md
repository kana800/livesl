<h3 align="center">This Project is **Archived**</h3>

### Why?

- `Web-Scraping` in general is a bit of "grey-area"
- The record label for majority of bands in the curated list `boom.sl` will make their own website. Plus Majority of their posts doesnt have relevant `description` which makes the `parser` obsolete.

The website will be **live** but the date isnt upto date;

---

<h3 align="center">Web-Scraper</h3>

- [Scraping](#scraper)
- [Bands, BandList](#band-list)
- [Parser](#parser)
    - [Parser Output/Input](#parser-output-with-normal-post-and-live-post)

### Scraper
> Web-Scraper component heavily relies on the [`instaloader`](https://github.com/instaloader/instaloader). 

**Instaloader** handles "scraping" all the content from the given `instagram_id`. The script will be only downloading the latest post of the listed *bands*.

<details>
<summary>
The scraped content will be downloaded to file directory scrapeddata
</summary>

```
scraper
|---scrapeddata
    |---owltreeo
    |---thesoulsrilanka
        |---2022-11-20_06-51-17_UTC.jpg // image of the post
        |---2022-11-20_06-51-17_UTC.json.xz 
        |---2022-11-20_06-51-17_UTC.txt //description of post
```
</details>

---

Only `Images` and `Descriptions` from the posts are saved to the `scraper/scrapeddata` directory. The **content** from the post `Descriptions` will be **analyzed** to identify whether the given post is about a live event. The file `meta.json` tracks *live events* for each *band*. For more information about the analysis of the post, read [parser.md](parser.md). 

#### Band List

The band list is loaded into the script in a `json` format. If you want to add the band just append the `instagram_id` of the band and the `band name`.

```json
{
    "bandnameid": "Band Name"
}
```
#### `Processed Information`

The processed information is **stored** in the `scraper/meta.json` file for generation of the static sites. The `json` file should normal look like this:

```json
{
    "bandid1": {
        "detected-date":"11/12/2023",
        "detected-price":"LKR 5000",
        "detected-location": "@Colombo",
        "post-link": "%link%"
    },
    "bandid2":{
        "detected-date":"12/12/2023",
        "detected-price":"LKR 4000",
        "detected-location": "@Kandy",
        "post-link": "%link%"
    }
}
```

---

### Usage

> Make sure all the modules from `requirements.txt` is installed

- It is *adviced* to simply `run.bat` file as it is the *"glue"* that connects all the *components* together.

```cmd
python wscrap.py --help 
```

---

### Parser

#### Parser Output with `Normal Post` and `Live Post`

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

This section explains how exactly the parser works. After a post is scraped we need to identify whether the given post has a "possibility" of being a **post about a live-event**. 

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