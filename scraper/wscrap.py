import instaloader
import sys
from datetime import datetime
from json import load, dumps
from pathlib import Path
from parser import IsLiveEvent

DEFAULT_DATA_PATH = Path('scraper/scrapeddata')
DEFAULT_JSON_PATH = Path('scraper/meta.json')
METAJSON = {
    'Dates': [],
    'Curr':[],
    'Location': []
}

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


def completeMetaDict(metadict):
    """summary: HELPER FUNCTION
    grabs necessary inputs for 
    metadict and return metadic
    args:
        metadict
    return:
        metadict
    """
    userinput = 1
    print("Enter 'n' or 'q' to exit\n")
    while (1):
        # i can write this much better later; for now
        # we will catch it like this
        if ((userinput == 'n') | (userinput == 'q')):
            break
        for k,v in metadict.items():
            if (len(v) == 0):
                userinput = input(f"Enter the {k}: ")
                metadict[k].append(userinput)
                if ((userinput == 'n') | (userinput == 'q')):
                    break
        return metadict


def getUserConfirmation(metadict, metastate, livestate):
    """summary: gets the user information
    about the post; If a post is not detected
    as live event or has incomplete information
    detect in metadict this function will be 
    called
    args:
        metadict -> metadict
        metastate -> state of meta dict
        live -> state of live event
    return:
        (bool, metadict);
    """
    userinput = 1
    while (userinput):
        if ((userinput == 'n') | (userinput == 'q')):
            break
        # both live event is false and metadict is incomplete
        if ((livestate == False) & (metastate == True)):
            inputstr = "live state seemed to fail and the meta dictionary is incomplete"
            userinput = input(f"{inputstr} Is this is a live event (Y->yes | N->no | Q->quit)?\n")
            if (userinput == 'Y'):
                print("lets complete the meta dictionary; You need to input these values manually...\n")
                metadict = completeMetaDict(metadict)
                return (True, metadict)
        elif (livestate == True & metastate == True):
        # only the meta dict is incomplete
            metadict = completeMetaDict(metadict)
            return (True, metadict)
        elif (livestate == False & metastate == False):
            userinput = input(f"Is this is a live event (Y->yes | N->no | Q->quit)?\n")
            if (userinput == 'Y'):
                return (True, metadict)
    return (False, metadict)


def IsMetaDictEmpty(metadict):
    """summary: returns whether
    meta dict is empty or not
    args:
        metadict -> metadict
    return:
        bool 
    """
    for v in metadict.values():
        if len(v) == 0:
            return True
    return False

def generateFiles(metadict):
    """summary: generate
    json files
    """
    with open(DEFAULT_JSON_PATH, 'w') as f:
        f.write(dumps(metadict, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    bandlist = loadBandList()
    print()
    metajson = {}
    L = instaloader.Instaloader(
        download_videos=False,
        download_video_thumbnails=False,
        filename_pattern="latest")
    for (key, value) in bandlist.items():
#        ret = downloadLatestPost(key)
        ret = 1
        # True New Post is Downloaded
        # Process It and Regenerate Meta.json
        if (ret):
            desc = grabContentDescription(key)
            (liveEvent, MetaDict)= IsLiveEvent(desc)
            state = IsMetaDictEmpty(MetaDict)
            if (state | liveEvent):
                (retuinf, MetaDict) = getUserConfirmation(MetaDict,
                metastate= state, livestate = liveEvent)
                if (retuinf):
                    metajson[key] = MetaDict
            print("live event -> ", liveEvent)
            print("Meta Dict  -> ", MetaDict)
    # generate meta.json file
    print("Generating Meta File\n")
    generateFiles(metajson)

