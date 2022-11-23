#---HASHTAGS---

testString1 = """this is a test string #dotdotay #dotnroll"""
hashonlyString1 = """#dotdotay #dotnroll"""
teststring1score = 0


testString2 = """planning is the best way but lorem 
got this together but cool random person people like
purple but purple not people
#thesoulsrilanka #album #ep #livemusic 
#originalmusic #srilanka #srilankanmusic #funding #trusting #appreciation 
#heartwarming #funding #sponsoring #wearethesoul #thankyou"""
hashonlyString2 = """#thesoulsrilanka #album #ep #livemusic #originalmusic #srilanka #srilankanmusic #funding #trusting #appreciation #heartwarming #funding #sponsoring #wearethesoul #thankyou""" 
teststring2score = 3

testString3 = """
sunara.music
Ahangama, Sri Lanka.

Home for the next 5 months.
Looking forward to playing music in the south coast of Sri Lanka once again.

Stay tuned for up coming gigs this week.

#gigs #djgig #ahangama #southcoastsrilanka #srilanka #paradies #islandlife #goodlife #beach #ocean
"""
hashonlyString3 = """#gigs #djgig #ahangama #southcoastsrilanka #srilanka #paradies #islandlife #goodlife #beach #ocean"""
teststring3score = 2


testString4 = """What are we doing, when we dont have gas, petrol and gigs?

Balang hitapalla.. just like all our other stuff..takes twice as long as we plan.

Thanks

#thesoulsrilanka #fruits #vegetables #tropicalfood #srilanka #influenza #music #srilankanmusic #vlog #blog #originalartists #itsashow #wecancooktoo #musiciansarecooks
"""
hashonlyString4 = """#thesoulsrilanka #fruits #vegetables #tropicalfood #srilanka #influenza #music #srilankanmusic #vlog #blog #originalartists #itsashow #wecancooktoo #musiciansarecooks"""
teststring4score = 2

teststringdict = {
    1: [testString1, hashonlyString1, teststring1score],
    2: [testString2, hashonlyString2, teststring2score],
    3: [testString3, hashonlyString3, teststring3score],
    4: [testString4, hashonlyString4, teststring4score],
}