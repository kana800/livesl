import instaloader
from datetime import datetime
from json import load
from pathlib import Path


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


if __name__ == "__main__":
    #TODO: add argparse
    bandlist = loadBandList()
    print()
    L = instaloader.Instaloader(
        download_videos=False,
        download_video_thumbnails=False)
    for (key, value) in bandlist.items():
        downloadLatestPost(key)
