<h3 align="center">This Project is Archived</h3>

### Why?

- `Web-Scraping` in general is a bit of "grey-area"
- The record label for majority of bands in the curated list `boom.sl` will make their own website. Plus Majority of their posts doesnt have relevant `description` which makes the `parser` obsolete.

> The website will be *live* but isnt upto date;

---

<!-- PROJECT LOGO -->
<br />
<p style="text-align: center" align="center">
  <a href="https://github.com/opensrilanka/livesl">
  </a>
  <span style='font-size:100px;'>&#127911;</span>
  <h3 align="center">Live SL</h3>
  <p align="center">
    <br />
    <a href="https://github.com/opensrilanka/livesl/projects">View Progress</a>
    ·
    <a href="https://github.com/opensrilanka/livesl/issues">Report Bug</a>
    ·
    <a href="https://github.com/opensrilanka/livesl/issues">Request Feature</a>
  </p>
</p>

---

### Summary

This project is a website that consist of list of latest live events from a curated [list of indie bands](bands.md) in srilanka.  

#### How It Work?

Github pages is being used for hosting a **static site** with the details of live events. The live events are **scraped** through the **social media** platforms of curated list of bands. 

#### Why?

Just wanted everything at one place for easier planning for attending live events. 

---

### Project Structure

`LiveSL` can be broken down into four main parts:

- [webscraper](scraper/README.md): Handles the web scraping
- [site-generator](sitegen/README.md): Handles template generation
- [website](): Consist of Documents for the website
- [glue](README.md#glue): Connects `webscraper`, `site-generator` and `website` together

<TODO add website branch here>

#### Adding a "Band" to the List

- You can simply raise an [issue]() if you want to add a band to the list. [For more information](scraper/README.md#band-list)
<TODO make a template for adding a certain band>

#### Glue

All the different components are connected together by the `run.bat` script. The following flowchart gives a brief idea on how the **glue stitches different modules together**.