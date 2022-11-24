"""
parser. The script will generate meta.json file;
"""
import re
import spacy
from collections import Counter


HASHTAGS = ["#liveevent", "#livemusic", 
"#srilanka" ,"#livemusicvenue",
"#live", "#event", "#gig"]
NOUNLIST = ["tickets", "gig", "entry", "music", "concert"]
VERBLIST = ["playing", "supporting", "coming"]
ENTITYLIST = ["DATE", "ORG", "MONEY", "ORDINAL",\
     "QUANITY", "CARDINAL", "TIME"]
MONTHLONG = ['january', 'february', 'march', 'april',\
    'may', 'june', 'july', 'august', 'september', 'october',\
    'november', 'december']
MONTHSHRT = ['jan', 'feb', 'mar', 'apr', 'may', 'june', 'july',\
    'aug', 'sept', 'oct', 'nov', 'dec']
WEEKLONG = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday',\
    'friday', 'saturday']
WEEKSHRT = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']

def IsInNouns(wrd):
    """summary:
    checks if the nouns
    is present in the word
    args:
        wrd -> tuple -> 
            ('noun', count)
    return:
        bool
    """
    wrd = wrd[0]
    for f in NOUNLIST:
        if len(wrd.split(f)) > 1:
            return True
    return False

def IsInMonth(wrd):
    """summary:
    checks if the months
    is present in the word
    args:
        wrd -> word you need to 
        check against
    return:
        bool
    """
    for f in MONTHLONG:
        if len(wrd.split(f)) > 1:
            return True
    for f in MONTHSHRT:
        if len(wrd.split(f)) > 1:
            return True
    return False

def IsInDays(wrd):
    """summary:
    checks if the months
    is present in the word
    args:
        wrd -> word you need to 
        check against
    return:
        bool
    """
    for f in WEEKLONG:
        if len(wrd.split(f)) > 1:
            return True
    for f in WEEKSHRT:
        if len(wrd.split(f)) > 1:
            return True
    return False

# loading spacy language model
nlp = spacy.load("en_core_web_sm")
# adding stopwords
STOPWORDS = nlp.Defaults.stop_words

def IsLiveEvent(description):
    """MainEntry
    summary: Helps us to determine
    whether the given post is a 
    live event or not;
    args:
        description -> description in
        the given post
    special:
        generates 'meta.json' if live
        event
    return:
        True/False
    """
    TotalScore = 0
    (htscore, htcnt) = scoreHashTags(description)
    # removing hashtags
    doc = nlp(removeHashTags(description))
    # scoring common words
    (cwscore, cwwrdcnt) = scoreCommonWords(doc)
    (nerscore, nerdetect) = scoreNamedEntities(doc)

    print(f"Hash Tag Score: {htscore, htcnt}\n")
    print(f"Common Word Score: {cwscore, cwwrdcnt}\n")
    print(f"NER Score: {nerscore, nerdetect}\n")
    print("---------------------------------\n")

#------------COMMON WORDS-------------------
def scoreCommonWords(doc):
    """summary: scores the common words
    args:
        doc -> spacy.tokens.doc.Doc
    return:
        int -> (totalscore, wordcount)
    """
    wordcnt = 5
    mcw = getMostCommonWords(doc, wordcnt)
    # expanding the dictionary
    nounlist = mcw["noun"]
    verblist = mcw["verb"]
    nounscore = 0 
    for wrd, cnt in nounlist:
        if wrd in NOUNLIST:
            nounscore += 1 
    verbscore = 0 
    for wrd, cnt in verblist:
        if wrd in VERBLIST:
            verbscore += 1 
    advscorenoun = list(map(IsInNouns, nounlist)).count(1)
    advscoreverb = list(map(IsInNouns, nounlist)).count(1)
    if advscorenoun > nounscore:
        nounscore = advscorenoun
    if advscoreverb > verbscore:
        nounscore = advscoreverb

    print("noun score -> ", advscorenoun)
    print("verb score -> ", advscorenoun)
    print(f"total score -> {nounscore + verbscore} / {wordcnt * 2}")
    return (nounscore + verbscore, wordcnt * 2)

def mostcommonwords(wrdlist, count):
    """
    summary: return list of most common
    words; The length of the list is determined
    by the count
    args:
        wrdlist -> list
        count -> int
    return 
        list
    """
    word_freq = Counter(wrdlist)
    return word_freq.most_common(count)  

def getMostCommonWords(doc, count):
    """summary: returns a dict
    of most 'count' amount of words
    args:
        doc -> spacy.tokens.doc.Doc
        count -> amount of words
    return:
        dict of most common words
        mcw = {
            "text": [],
            "noun": [],
            "verb": []
        }
    """
    mcw = {}
    # tokens that arent stop words or punctuations or whitespace
    textwords = [token.text for token in doc
                 if not token.is_stop and not token.is_punct
                 and not token.is_space]
    # tokens that are nouns
    nounwords = [token.text for token in doc
                 if not token.is_stop and not token.is_punct
                 and token.pos_ == "NOUN"]
    # tokens that are verbs
    verbwords = [token.text for token in doc
                 if not token.is_stop and not token.is_punct
                 and not token.is_space and token.pos_ == "VERB"]
    
    mcw["text"] = mostcommonwords(textwords, count)
    mcw["noun"] = mostcommonwords(nounwords, count)
    mcw["verb"] = mostcommonwords(verbwords, count)
    return mcw

#-----------NAMED ENTITIES------------------
def scoreNamedEntities(doc):
    """score named entities
    args:
        doc -> spacy.tokens.doc.Doc
    return:
        (score, totalkeywords) -> (int, int) 
    """
    # ORDINAL -> 1st, 2nd, 3rd
    # CARDINAL -> NUMBERALS DONT FALL UNDER OTHER TYPES
    # DATE -> DATE
    # holds the detectedDates
    score = 0
    detectedDates = []
    detectedCurrency = []
    detectedLocations = []
    for span in doc.ents:
        # checking if preferred entities are 
        # present
        if span.label_ in ENTITYLIST:
            # checking if the given input is date
            if ((span.label_ == "ORDINAL") or (span.label_ == "DATE")):
                ret = IsDate(span)
                # checking if date is detected or not
                if ret != None: detectedDates.append(ret)
            elif (span.label_ == "CARDINAL"):
                (ret, retstr) = detectCardinalType(span)
                # checking if date is detected or not
                if ret == "Cur":
                     detectedCurrency.append(retstr)
                elif ret == "Date":
                    detectedDates(retstr)

    # final hard checks for currencies and location
    if (len(detectedCurrency) == 0):
        ret = IsCurrencyDesc(doc.text)
        if ret != None: detectedCurrency.append(ret)

    # scoring the dates and currency
    # one point is given even if there is
    # multiple detections
    score += 1 if len(detectedCurrency) >= 1 else 0
    score += 1 if len(detectedDates) >= 1 else 0

    return (score, len(doc.ents))

def detectCardinalType(span):
    """summary: detects type of cardinal
    and try to extract information
    args:
        span -> spacy.tokens.doc.Doc
    return:
        (type, str)
        type -> None | "Date" | "Cur"
        str -> if a text is identified
    """
    if (span.label_ == "CARDINAL"):
        currstr = IsCurrency(span)
        # Bad Style Coding; Will Change Later
        if currstr != None: return ("Cur", currstr)
        datestr = IsDate(span)
        if datestr != None: return ("Date", datestr)
        return (None,"")
    else:
        return (None,"")

def IsDate(span):
    """summary: return whether the
    given combination of span tokens
    is a date or isnt;
    args:
        span -> spacy.tokens.doc.Doc
    return:
        if no date is found -> None
        if date is detected -> str
    """
    # ORDINAL -> 1st, 2nd, 3rd
    # CARDINAL -> NUMBERALS DONT FALL UNDER OTHER TYPES
    # DATE -> DATE
    if span.label_ == "DATE":
        foundmonth = [1 for i in str.lower(span.text).split(" ") \
            if i in MONTHLONG or i in MONTHSHRT].count(1)
        founddate = [1 for i in str.lower(span.text).split(" ") \
            if i in WEEKLONG or i in WEEKSHRT].count(1)
        foundyear = len(re.findall(r"\d{4}",str.lower(span.text)))
        if ((foundmonth > 0) & (foundyear > 0)):
            # possibility of having month and year 
            # possibility of a complete date
            sanitizetxt = sanitizeString(span.text)
            return sanitizetxt
    elif span.label_ == "ORDINAL":
        # possibility of having a day mentioned
        foundday = len(re.findall(r"\d", str.lower(span.text)))
        if (foundday > 0):
            sanitizetxt = sanitizeString(span.text)
            return sanitizetxt
    else:
        # possibility of having a month or day mentioned
        # in text
        foundmonth = IsInMonth(span.text) 
        foundday = IsInDays(span.text)
        if ((foundday) | (foundmonth)): return sanitizeString(span.text)
        return None

def IsCurrency(span):
    """summary: return whether the
    given combination of span tokens
    is a currency;
    args:
        span -> spacy.tokens.doc.Doc
    return:
        if no currency is found -> None
        if currency is detected -> str
    """
    sanitizedstr = sanitizeString(span.text)
    foundcurrency = len(
        re.findall(r"(LKR|Rs|\$)[\s|\d]\d*", sanitizedstr))
    foundcurrencytag = len(
        re.findall(r"(LKR|Rs|\$)", sanitizedstr))
    if foundcurrency > 0:
        return sanitizedstr
    if foundcurrencytag > 0:
        return sanitizedstr
    return None 

def IsCurrencyDesc(str):
    """summary: return whether the
    given string consist of currency;
    args:
        str -> string
    return:
        if no currency is found -> None
        if currency is detected -> str
    """
    foundcurrency = re.findall(r"(LKR|Rs|\$)[\s|\d]\d*", str)
    foundcurrencytag = re.findall(r"(LKR|Rs|\$)", str)
    if ((len(foundcurrency) > 0) | len(foundcurrencytag) > 0):
        return " ".join(foundcurrency)

def sanitizeString(text):
    """summary: removes stop
    words and punctuations from
    a string
    args:
        text -> str
    return:
        str
    """
    lst=[]
    for token in text.split():
        if token.lower() not in STOPWORDS: 
            lst.append(token)
    return " ".join(lst)
        
#-------------HASHTAGS----------------
def scoreHashTags(description):
    """
    summary: Scores the HashTags
    in the given post
    args:
        description -> description
        in the given post
    return:
        score
    """
    print("---ScoreHashTags---")
    thashtags = scrapeHashTags(description)
    ttotalkeywords = len(thashtags)
    score = 0
    for h in thashtags:
        if h in HASHTAGS:
            score += 1 
    # advanced checking
    advscore = list(map(IsInHashTags, thashtags))
    # check if the adv score is greater
    if advscore.count(1) > score:
        score = advscore.count(1)
    print(f"total score -> {score}" 
    f" | total hashtags detected -> {ttotalkeywords}")
    return (score, ttotalkeywords)

def IsInHashTags(wrd):
    """summary:
    checks if the hashtag
    is present in the word
    args:
        wrd -> word you need to 
        check against
    return:
        bool
    """
    for f in HASHTAGS:
        if len(wrd.split(f)) > 1:
            return True
    return False

def scrapeHashTags(description):
    """HelperFunction->ScoreHashTags
    summary: Scrapes the 
        HashTags in a given post.
    args: 
        description -> description in 
        the given post
    return:
        list of hashtags
    """
    return re.findall(
        r"\B(\#[a-zA-Z]+\b)(?!;)",
         description)

def removeHashTags(description):
    """HelperFunction->ScoreHashTags
    summary: Removes the 
        HashTags in a given post.
    args: 
        description -> description in 
        the given post
    return:
        string without hashtags
    """
    return re.sub(
        r"\B(\#[a-zA-Z]+\b)(?!;)", 
        "", description)