## Web-Scraper



### Summary
> Web-Scraper heavily relies on the [`instaloader`](https://github.com/instaloader/instaloader). 

**Instaloader** handles "scraping" all the content from the given `instagram_id`. The script will be only downloading the latest post of the listed *bands*. The scraped content will be downloaded to file directory `scrapeddata`.

Only `Images` and `Descriptions` from the posts are saved to the `scraper/scrapeddata` directory. The **content** from the post `Descriptions` will be **analyzed** to identify whether the given post is about a live event. The file `meta.json` tracks *live events* for each *band* 

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

#### Post Scoring and Live Events
<This is work in progress>

> How are we going to determine whether the given post is a *live event* or not ?

This project will use **scoring system** to identify whether given post is a *live event*. 

- Most post with **live music venues** has a several hashtags in its posts. Like 
`#livemusicvenue #livemusicevent`. Post like this will be given a point
- Post that mention **prices** will be given a point. These prices should be mentioned will several keywords
- Post that mention **Date** will be given a point. The given dates should have proper meaning.


---

### Usage

> Make sure all the modules from `requirements.txt` is installed

- It is *adviced* to simply `run.bat` file as it is the *"glue"* that connects all the *components* together.

```cmd
python wscrap.py --help 
```