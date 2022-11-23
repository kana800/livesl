"""
parser. The script will generate meta.json file;
"""
import re
import spacy
from collections import Counter


HASHTAGS = ["#liveevent", "#livemusic", 
"#srilanka" ,"#livemusicvenue",
"#live", "#event", "#gig"]

NOUNLIST = ["gig", "entry", "music", "concert"]
VERBLIST = ["playing", "supporting", "coming"]
ENTITYLIST = ["DATE", "ORG", "MONEY", "ORDINAL", "QUANITY", "CARDINAL", "TIME"]

nlp = spacy.load("en_core_web_sm")

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
    doc = nlp(description)


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

def scoreNamedEntities(doc):
    """score named entities
    args:
        doc -> spacy.tokens.doc.Doc
    return:
        int -> score 
    """
    return False

def getNamedEntities(doc):
    """
        doc -> spacy.tokens.doc.Doc
    return:
        int -> score 
    """
    for span in doc.ents:
        # checking if preferred entities are 
        # present
        print("sentence ", span.sent)
        if span.label_ in ENTITYLIST:
            print(span.text,
            "|" ,span.label_,
            "|" ,spacy.explain(span.label_))
            lefts = [t.text for t in span.lefts]
            rights = [t.text for t in span.rights]
            print("lefts ", lefts)
            print("rights ", rights)

    return False

def IsDate(span, lefts, rights):
    """summary: return whether the
    given combination of span tokens
    is a date;
    args:
        span
        lefts -> list -> left span tokens
        rights -> list ->right span token
    return:
        [bool, str]
    """
    
    


def scoreSpecialCases(description):
    """
    """
    return False

def getSpecialCases(description):
    """
    """
    return False

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