### Parser

This document explains how exactly the parser works. After a post is scraped we need to identify whether the given post has a "possibility" of being a **post about a live-event**. Several **bands** has added `hashtags` like `live-events` or `liveevents` to the description of the post.

We will be scoring the posts according to several key points and we will be using `nltk` for further analysis of the given description. 

