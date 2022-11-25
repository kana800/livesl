import instaloader
import sys
from datetime import datetime
from json import load
from pathlib import Path
from parser import IsLiveEvent

DEFAULT_DATA_PATH = Path('scraper/scrapeddata')

def loadBandList():
    """
    summary: load the band list and ret
    dictionary
    return:
        dictionary consist band info
    """
    filename = "scraper\\bands.json"
    f = open(filename,'r')
    return load(f)

def downloadLatestPost(bandname):
    """
    summary: downloads the latest 
    post for the given band name
    args:
        bandname -> string 
    return:
        True/False
    """
    temppath = DEFAULT_DATA_PATH/bandname
    posts = instaloader.Profile.from_username(
        L.context, bandname).get_posts()

    for post in posts:
        # obtain only the latest post
        # TODO: find more effcient way to obtain the 
        # latest post
        result = L.download_post(post, temppath)
        break
    return result

def grabContentDescription(bandname):
    """summary: grabs the content
    description and returns a string
    args:
        bandname -> string
    return:
        description -> string
    """
    readpath = DEFAULT_DATA_PATH/bandname/"latest.txt"
    with open(readpath, 'r') as f:
        contents = f.readlines()
    return " ".join(contents)


if __name__ == "__main__":
    bandlist = loadBandList()
    print()
    L = instaloader.Instaloader(
        download_videos=False,
        download_video_thumbnails=False,
        filename_pattern="latest")
    for (key, value) in bandlist.items():
        ret = downloadLatestPost(key)
        # True New Post is Downloaded
        # Process It and Regenerate Meta.json
        if (ret):
            desc = grabContentDescription(key)
            (liveEvent, MetaDict)= IsLiveEvent(desc)
            print("live event -> ", liveEvent)
            print("Meta Dict  -> ", MetaDict)