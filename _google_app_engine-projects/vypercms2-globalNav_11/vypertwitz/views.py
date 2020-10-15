import time
import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, ugettext as __
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object, update_object
from google.appengine.ext import db
from mimetypes import guess_type
from django.template import loader
from django.template import Context

from ragendja.dbutils import get_object_or_404
from ragendja.template import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site, RequestSite

from random import choice, sample
from google.appengine.api import memcache

from vyperlogix.google.gae import unique

from vyperlogix.hash.lists import HashedLists2

from vyperlogix.misc import ObjectTypeName

import models

import re

import md5

import mimetypes

import logging

from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc import _utils
from vyperlogix.django import django_utils
from vyperlogix.hash import lists

from vyperlogix.enum.Enum import Enum

from vyperlogix.socials.tweets import Tweepy
from vyperlogix.url import tiny
from vyperlogix.socials.tweepy.error import TweepError

__mimetype = mimetypes.guess_type('.html')[0]

_title = 'Vyper Logix Corp, The 21st Century Python Company'

__product__ = 'VyperTwitz&trade;'
__version__ = '1.0.0.0'

__content__ = '''{{ content }}'''

status = {'success':False}

__TweepError__ = 'TweepError'
__typez__ = 'word_types'
__wordz__ = 'words'

__adverbs__ = '''["unfortunately", "yawningly", "warmly", "enormously", "heavily", "coolly", "upbeat", "irritably", "quietly", "naturally", "openly", "questioningly", "knowledgeably", "sleepily", "carefully", "hastily", "weakly", "uselessly", "poorly", "victoriously", "certainly", "busily", "painfully", "majestically", "coaxingly", "actually", "readily", "kissingly", "deliberately", "unnecessarily", "excitedly", "foolishly", "yieldingly", "carelessly", "daintily", "adventurously", "instantly", "regularly", "eventually", "joshingly", "generously", "broadly", "far", "famously", "kiddingly", "courageously", "soon", "enthusiastically", "selfishly", "ferociously", "nearly", "closely", "dearly", "not", "immediately", "jaggedly", "loyally", "wisely", "kindly", "easily", "overconfidently", "keenly", "nicely", "always", "interestingly", "anxiously", "acidly", "accidentally", "swiftly", "oddly", "annually", "frantically", "softly", "fully", "zestfully", "delightfully", "voluntarily", "energetically", "seldom", "silently", "owlishly", "unabashedly", "calmly", "quicker", "miserably", "often", "badly", "physically", "loosely", "upliftingly", "successfully", "worriedly", "nervously", "unexpectedly", "likely", "quaintly", "kindheartedly", "cleverly", "stealthily", "optimistically", "righteously", "really", "even", "hourly", "ultimately", "rarely", "mechanically", "sweetly", "unnaturally", "deeply", "tenderly", "continually", "rightfully", "seriously", "lazily", "correctly", "usefully", "patiently", "fondly", "violently", "crossly", "healthily", "jubilantly", "never", "valiantly", "knavishly", "promptly", "gratefully", "inwardly", "abnormally", "intensely", "bashfully", "wearily", "lovingly", "shakily", "joyfully", "sympathetically", "noisily", "freely", "searchingly", "commonly", "vivaciously", "innocently", "boldly", "boastfully", "greatly", "reluctantly", "arrogantly", "judgementally", "upward", "fatally", "blissfully", "solidly", "yearly", "rudely", "equally", "afterwards", "thankfully", "diligently", "suddenly", "playfully", "angrily", "unethically", "highly", "quarrelsomely", "merrily", "inquisitively", "officially", "lively", "doubtfully", "thoughtfully", "quickly", "tomorrow", "truly", "cheerfully", "upside-down", "truthfully", "sadly", "rapidly", "restfully", "monthly", "reassuringly", "strictly", "smoothly", "only", "fast", "greedily", "frenetically", "loftily", "faithfully", "slowly", "too", "bitterly", "speedily", "mockingly", "perfectly", "urgently", "intently", "justly", "solemnly", "gleefully", "mostly", "queasily", "happily", "exactly", "vaguely", "yearningly", "gently", "shrilly", "curiously", "powerfully", "repeatedly", "sharply", "blindly", "upright", "gladly", "vacantly", "questionably", "wholly", "positively", "partially", "willfully", "upwardly", "cruelly", "frankly", "wonderfully", "tremendously", "scarily", "needily", "queerly", "zealously", "cautiously", "safely", "vastly", "kookily", "surprisingly", "sternly", "elegantly", "more", "separately", "vainly", "brightly", "bravely", "rigidly", "lightly", "almost", "bleakly", "shyly", "politely", "punctually", "tensely", "dreamily", "wildly", "knottily", "fiercely", "gracefully", "beautifully", "yesterday", "recklessly", "tightly", "mysteriously", "clearly", "reproachfully", "unimpressively", "zestily", "dimly", "jealously", "hungrily", "terribly", "fortunately", "thoroughly", "quizzically", "wetly", "generally", "limply", "helpfully", "jovially", "loudly", "potentially", "defiantly", "madly", "suspiciously", "unaccountably", "joyously", "unbearably", "meaningfully", "fairly", "briefly", "furiously", "sedately", "less", "mortally", "deceivingly", "neatly", "hopelessly", "usually", "quirkily", "absentmindedly", "sheepishly", "seemingly", "fervently", "woefully", "utterly", "youthfully", "wrongly", "knowingly", "extremely", "awkwardly", "colorfully", "scarcely", "offensively", "especially", "viciously", "frightfully", "triumphantly", "obnoxiously", "longingly", "sometimes", "well", "roughly", "daily", "helplessly", "verbally", "properly", "honestly", "very", "obediently", "briskly", "evenly"]'''
__prepositions__ = '''["over", "through", "before", "in place of", "except", "impatient with", "to", "under", "save", "worth", "versus", "around", "outside", "rewarded for", "along with", "underneath", "despite", "during", "regarding", "like", "excluding", "beneath", "round", "because of", "past", "beyond", "out", "capable of", "for", "since", "excepting", "near", "per", "behind", "above", "between", "across", "in addition to", "instead of", "in case of", "besides", "along", "by", "on", "about", "of", "against", "times", "plus", "aboard", "onto", "in back of", "among", "via", "into", "within", "down", "according to", "anti", "except for", "throughout", "considering", "from", "amidst", "next", "until", "superior to", "concerning", "but", "with", "than", "absent", "familiar with", "unlike", "inside", "up", "below", "following", "toward", "minus", "in spite of", "alongside", "as", "at", "in", "in front of", "mid", "beside", "till", "up to", "on top of", "out of", "atop", "apart from", "towards", "opposite", "after", "upon", "off", "by means of", "amid", "without", "as for"]'''
__pronouns__ = '''["all", "everyone", "what", "theirs", "some", "it", "whatever", "one", "nothing", "himself", "yourself", "something", "another", "each other", "our", "themselves", "any", "you", "she", "everybody", "whose", "little", "her", "everything", "whoever", "who", "its", "anyone", "few", "much", "which", "ours", "neither", "several", "yourselves", "more", "them", "his", "somebody", "that", "nobody", "none", "mine", "most", "we", "whichever", "they", "others", "hers", "yours", "no one", "herself", "him", "those", "he", "me", "both", "myself", "your", "one another", "anything", "these", "many", "anybody", "us", "whomever", "their", "this", "someone", "itself", "either", "ourselves", "each", "my", "other", "whom"]'''
__verbs__ = '''["represent", "coach", "consider", "dance", "scratch", "rob", "invent", "wrestle", "sleep", "battle", "follow", "hate", "milk", "forget", "compose", "depend", "calculate", "uphold", "recruit", "unpack", "flash", "scold", "send", "tickle", "charge", "moor", "skip", "smile", "dislike", "include", "ride", "inject", "fly", "fax", "rescue", "dispense", "rise", "rhyme", "induce", "wave", "shoot", "foretell", "mourn", "decide", "bleach", "unify", "trouble", "shear", "wipe", "arrange", "succeed", "level", "tear", "pinch", "conceive", "dig", "list", "leave", "race", "delegate", "enhance", "enforce", "shoe", "enjoy", "chew", "overdo", "force", "regret", "fence", "sigh", "direct", "transform", "sign", "jump", "fold", "rate", "cost", "design", "go", "pass", "bake", "employ", "educate", "poke", "hide", "appear", "wreck", "rot", "squeeze", "brief", "melt", "verbalize", "crush", "experiment", "suspect", "conduct", "upset", "reply", "exercise", "satisfy", "edited", "inspect", "led", "wail", "modify", "punch", "water", "shape", "entertain", "let", "sink", "address", "sing", "change", "wait", "box", "convert", "boast", "institute", "slow", "study", "whine", "reason", "bow", "queue", "harass", "mentor", "grease", "permit", "implement", "pack", "explain", "foresee", "divide", "forbid", "win", "manage", "prefer", "replace", "put", "vex", "establish", "post", "manipulate", "overhear", "zip", "injure", "paste", "motivate", "visit", "irritate", "generate", "process", "live", "doubt", "call", "shed", "recommend", "strike", "type", "tell", "breathe", "shine", "flap", "relax", "afford", "impress", "reign", "hurt", "warn", "excuse", "drown", "stick", "hold", "scribble", "annoy", "join", "challenge", "pretend", "stroke", "pour", "reproduce", "remain", "hope", "install", "learn", "meet", "arrive", "fetch", "attain", "control", "claim", "compare", "tap", "shade", "give", "predict", "lock", "sense", "share", "accept", "slit", "bend", "slip", "arise", "hit", "keep", "dress", "occur", "guarantee", "normalize", "sip", "end", "memorize", "sit", "provide", "attract", "travel", "damage", "pine", "delay", "worry", "cling", "reject", "answer", "stir", "sin", "classify", "sweat", "suffer", "map", "plant", "attend", "watch", "dive", "spot", "sneak", "reflect", "catalog", "produce", "lay", "pat", "suck", "grow", "man", "purchase", "refuse", "appraise", "attempt", "remember", "correlate", "whistle", "bind", "amuse", "appreciate", "arbitrate", "greet", "stimulate", "mislead", "inform", "switch", "maintain", "jail", "deceive", "enter", "offend", "operate", "dream", "order", "talk", "whip", "blind", "help", "sprout", "peck", "govern", "disarm", "tempt", "trade", "suspend", "program", "shake", "stride", "perfect", "write", "shock", "monitor", "fit", "decay", "pray", "wring", "fix", "hypothesize", "thrust", "choose", "fade", "carve", "release", "overcome", "split", "fool", "crash", "finance", "fling", "nod", "dam", "press", "practice", "earn", "introduce", "break", "interview", "bang", "spill", "rank", "kiss", "interrupt", "spend", "flee", "complain", "expedite", "enacted", "administer", "execute", "name", "wash", "troubleshoot", "drop", "synthesize", "explode", "handwrite", "slide", "trap", "rock", "marry", "scorch", "mean", "consolidate", "improvise", "harm", "activate", "retrieve", "sow", "formulate", "bump", "strip", "reduce", "unlock", "expect", "undertake", "measure", "happen", "extract", "wander", "tabulate", "clothe", "try", "accomplish", "stitch", "open", "confess", "abide", "research", "increase", "sparkle", "encourage", "mate", "adapt", "mend", "print", "lecture", "illustrate", "cause", "correct", "shut", "assist", "profess", "hang", "utilize", "contain", "forgive", "clarify", "qualify", "streamline", "verify", "imagine", "ask", "embarrass", "estimate", "cough", "knit", "bleed", "care", "swell", "rehabilitate", "overtake", "launch", "conceptualize", "initiate", "place", "swing", "blush", "facilitate", "scare", "feed", "sew", "organize", "render", "prevent", "feel", "relate", "confuse", "number", "fancy", "blink", "hook", "instruct", "carry", "radiate", "ring", "tame", "miss", "summarize", "warm", "engineer", "moan", "guess", "service", "paint", "bite", "breed", "tow", "construct", "attach", "attack", "shiver", "draft", "ruin", "dwell", "weave", "boil", "listen", "hug", "overdraw", "misspell", "hum", "acquire", "park", "innovate", "discover", "broadcast", "part", "telephone", "consult", "copy", "crawl", "officiate", "specify", "nail", "photograph", "translate", "target", "double", "anticipate", "beg", "project", "matter", "persuade", "endure", "light", "proofread", "bet", "exhibit", "lick", "subtract", "clip", "slay", "strengthen", "navigate", "plead", "mine", "slap", "say", "murder", "need", "thaw", "regulate", "saw", "unfasten", "invite", "sell", "lie", "groan", "soak", "wink", "snow", "note", "mix", "tick", "build", "punish", "praised", "destroy", "divert", "wonder", "begin", "altered", "allow", "trace", "serve", "object", "reach", "chart", "admire", "preset", "plan", "precede", "multiply", "coil", "snatch", "publicize", "muddle", "glow", "upgrade", "clear", "camp", "cover", "drive", "face", "wind", "clean", "weigh", "scream", "shop", "think", "bomb", "inspire", "show", "cheat", "alight", "reorganize", "retire", "bring", "paddle", "participate", "fear", "label", "seal", "find", "transport", "trot", "pick", "wriggle", "pause", "tire", "dramatize", "pump", "bust", "jam", "integrate", "announce", "stain", "achieve", "do", "move", "handle", "get", "beat", "lighten", "express", "stop", "perceive", "bear", "yawn", "beam", "report", "intensify", "smash", "bat", "resolve", "cry", "borrow", "remove", "gather", "investigate", "stuff", "kneel", "ascertain", "ban", "kill", "grab", "steal", "audited", "preach", "respond", "withstand", "forego", "set", "burst", "frame", "freeze", "trick", "reinforce", "bare", "polish", "fail", "close", "hammer", "concern", "detect", "record", "review", "sail", "please", "forecast", "realign", "mug", "disprove", "progress", "juggle", "forsake", "preserve", "notice", "extend", "smite", "prescribe", "deliver", "interfere", "spray", "cut", "spare", "wear", "spoil", "jog", "spark", "comb", "come", "improve", "protect", "store", "drum", "sniff", "license", "joke", "systemize", "contract", "agree", "assure", "admit", "concentrate", "misunderstand", "sketch", "buzz", "swim", "argue", "approve", "load", "suggest", "conclude", "color", "acted", "solve", "pop", "walk", "whisper", "laugh", "trust", "reconcile", "quit", "raise", "stamp", "wobble", "create", "recognize", "mark", "taste", "gaze", "interpret", "interest", "frighten", "fry", "tug", "empty", "define", "dry", "spit", "withhold", "fire", "shave", "overthrow", "excite", "search", "observe", "awake", "turn", "catch", "last", "spin", "present", "pilot", "applied", "twist", "save", "symbolize", "look", "dissect", "originate", "budget", "nominate", "compile", "cast", "suppose", "match", "scatter", "balance", "wake", "guide", "mistake", "supply", "bathe", "stink", "disapprove", "sting", "tease", "brake", "return", "rid", "vanish", "conserve", "disappear", "chase", "whirl", "develop", "steer", "perform", "pay", "make", "belong", "cross", "unite", "trip", "inventory", "see", "propose", "advise", "scrub", "settle", "smoke", "itch", "screw", "applaud", "nest", "drink", "disagree", "negotiate", "rain", "alert", "delight", "dust", "pedal", "weep", "expand", "cycle", "insure", "drain", "kept", "drip", "grind", "cheer", "command", "withdraw", "coordinate", "model", "rush", "justify", "restructure", "sound", "distribute", "bruise", "obtain", "beset", "judge", "select", "identify", "touch", "love", "glue", "speed", "secure", "blow", "oriented", "blot", "wed", "point", "wet", "realize", "arrest", "add", "spread", "grin", "crack", "input", "hurry", "possess", "ski", "kick", "take", "grip", "hover", "march", "finalize", "read", "evaluate", "bid", "mow", "sweep", "know", "knot", "supervise", "interlay", "strap", "dare", "knock", "snore", "like", "confront", "seek", "hunt", "zoom", "shrink", "ignore", "collect", "continue", "lose", "become", "signal", "clap", "exceed", "wend", "deal", "tumble", "understand", "spring", "back", "bounce", "soothsay", "accelerate", "escape", "critique", "prick", "bore", "creep", "shrug", "bless", "string", "pinpoint", "lead", "remind", "avoid", "separate", "lean", "thank", "pioneer", "leap", "behave", "eliminate", "speak", "refer", "locate", "be", "run", "obey", "peel", "schedule", "rub", "tour", "burn", "communicate", "use", "procure", "market", "bolt", "assemble", "peep", "stay", "bury", "throw", "tread", "plug", "simplify", "prove", "choke", "surround", "thrive", "chop", "stretch", "swear", "ensure", "stand", "meddle", "revise", "repair", "own", "undergo", "owe", "float", "lifted", "assess", "guard", "transcribe", "promise", "brush", "determine", "apologize", "wrap", "risk", "stare", "rely", "rejoice", "log", "prepare", "tutor", "transfer", "support", "question", "mediate", "long", "fight", "start", "suit", "inlay", "analyze", "bubble", "treat", "manufacture", "step", "head", "buy", "complete", "form", "offer", "heal", "teach", "undress", "heat", "hear", "heap", "grate", "overflow", "promote", "eat", "count", "pull", "counsel", "waste", "compute", "consist", "hop", "wish", "work", "preside", "decorate", "hand", "demonstrate", "display", "x-ray", "connect", "diagnose", "sort", "adopt", "play", "devise", "flow", "describe", "influence", "haunt", "sublet", "soothe", "examine", "cure", "exist", "file", "request", "strive", "curl", "enlist", "tremble", "check", "film", "fill", "sack", "spell", "want", "deserve", "tip", "detail", "scrape", "graduate", "flood", "book", "terrify", "branch", "test", "tie", "behold", "smell", "roll", "draw", "repeat", "intend", "sling", "lend", "shelter", "surprise", "slink", "welcome", "update", "squash", "drag", "flower", "puncture", "squeak", "sneeze", "desert", "structure", "squeal", "appoint", "land", "phone", "curve", "rule", "untidy", "train", "compete", "rinse", "time", "push", "fasten", "yell", "receive", "restored"]'''

from django.utils import simplejson
__words__ = {}
__words__['adverbs'] = simplejson.loads(__adverbs__)
__words__['prepositions'] = simplejson.loads(__prepositions__)
__words__['pronouns'] = simplejson.loads(__pronouns__)
__words__['verbs'] = simplejson.loads(__verbs__)

__spice__ = '(Read to win $100 USD.)'

def python_to_json(obj):
    from django.utils import simplejson

    json = simplejson.dumps(obj)

    return json.replace('\n','')

def _doTweets(request,parms):
    from vyperlogix.feeds import feedparser
    global status
    status = {'success':False}
    feeds = models.RssFeed.all()
    if (feeds.count() > 0):
        try:
            aFeed = choice(feeds)

            d = feedparser.parse(aFeed.link.url)
            notChosen = True
            while (notChosen):
                usedlinks = models.UsedLink.all().filter('feed',aFeed)
                used = [l.url for l in usedlinks]
                d_entries = HashedLists2()
                for e in d['entries']:
                    d_entries[e.link] = e
                for u in used:
                    del d_entries[u]
                l_entries = []
                for k,v in d_entries.iteritems():
                    l_entries.append(v)
                try:
                    anEntry = choice(l_entries)
                    status['entry'] = {}
                    for k,v in anEntry.iteritems():
			_hasDict = False
			try:
			    d = v.__dict__
			    _hasDict = True
			except:
			    pass
                        status['entry'][k] = list(v) if (ObjectTypeName.typeClassName(v) == 'tuple') else v if (not _hasDict) else v.__dict__
                    aUsedLink = models.UsedLink(feed=aFeed,url=anEntry.link)
                    aUsedLink.save()
                    linkstats = models.UsedLinkStat.all().filter('feed',aFeed).filter('url',anEntry.link)
                    if (linkstats.count() > 0):
                        for aLinkStat in linkstats:
                            aLinkStat.count += 1.0
                            aLinkStat.save()
                    else:
                        aLinkStat = models.UsedLinkStat(feed=aFeed,url=anEntry.link,count=1.0)
                        aLinkStat.save()
                    notChosen = False
                    status['success'] = True
                except IndexError:
                    for aUsedLink in usedlinks:
                        aUsedLink.delete()
        except Exception, e:
            info_string = _utils.formattedException(e)
            status['message'] = info_string
    else:
        status['reason'] = 'There are no feeds define.'
    return status

def doTweets(request,parms):
    status = _doTweets(request,parms)
    s_response = python_to_json(status)
    return s_response

def default(request,path):
    try:
        s_response = ''
        __error__ = ''

        parms = django_utils.parse_url_parms(request)

        isTweets = (len(parms) >= 2) and (parms[0:2] == [u'vypertwitz', u'tweet']) # /vypertwitz/tweet/
        isTweetz = (len(parms) >= 4) and (parms[0:2] == [u'vypertwitz', u'tweetz']) # /vypertwitz/tweetz/username/password/
        isWordz = (len(parms) == 2) and (parms[0:2] == [u'vypertwitz', u'wordz']) # /vypertwitz/wordz/
        mimetype = mimetypes.guess_type('.json')[0]
        if (isTweets):
            s_response = doTweets(request,parms)
	elif (isTweetz):
	    from vyperlogix.products.keys import _decode
	    username = _decode(parms[2])
	    password = _decode(parms[3])
            _status = _doTweets(request,parms)
	    url = tiny.unu(_utils.ascii_only(_status['entry']['link']))
	    _msg = _utils.ascii_only(_status['entry']['title'])
	    aWord = 'hidden wumpus'
	    if (__spice__.find('%') > -1):
		types = memcache.get(__typez__)
		if (not types):
		    types = [t.word_type for t in models.WordType.all()]
		    memcache.set(__typez__, types, time=3600)
		if (len(types) > 0):
		    words = memcache.get(__wordz__)
		    if (not words):
			d_words = lists.HashedLists()
			def handleWords(k,v):
			    d_words[k] = v
			for w in models.Word.all():
			    handleWords(w.word_type.word_type,w.word)
			words = d_words.asDict()
			memcache.set(__wordz__, words, time=3600)
		    if (len(words) > 0):
			aType = choice(words.keys())
			aWord = choice(words[aType])
		spice = __spice__ % (aWord)
	    else:
		spice = __spice__
	    serial = '%15.5f' % (time.time())
	    nMax = 134-len(url)-len(spice)-len(serial)
	    msg = _msg[0:nMax]+('...' if (len(_msg) > nMax) else '')
	    s = '%s "%s" %s %s' % (serial,msg,url,spice)
	    _id = '%s_%s' % (__TweepError__,md5.new(_status['entry']['links'][0]['href']).hexdigest())
	    isTweepError = memcache.get(_id)
	    logging.debug('default.isTweetz.1 :: isTweepError=%s' % (isTweepError))
	    if (not isTweepError):
		try:
		    Tweepy.update_status(username,password,s)
		    memcache.set(_id, False, time=3600)
		    logging.debug('default.isTweetz.2 :: isTweepError=False')
		except TweepError, e:
		    memcache.set(_id, True, time=3600)
		    logging.debug('default.isTweetz.3 :: isTweepError=True, (%s)' % (e))
            s_response = python_to_json(_status)
	elif (isWordz):
	    types = models.WordType.all()
	    status = {'types.1':types.count()}
	    logging.debug('default.isWordz.1 :: types.count()=%s' % (types.count()))
	    if (types.count() == 0):
		for w in __words__.keys():
		    aWordType = models.WordType(word_type=w)
		    aWordType.save()
		types = models.WordType.all()
		status['types.2'] = types.count()
		logging.debug('default.isWordz.2 :: types.count()=%s' % (types.count()))
	    words = models.Word.all()
	    status['words.1'] = words.count()
	    logging.debug('default.isWordz.3 :: words.count()=%s' % (words.count()))
	    for k,v in __words__.iteritems():
		_types = models.WordType.all().filter('word_type',k)
		logging.debug('default.isWordz.4 :: word_type=%s, _types.count()=%s' % (k,_types.count()))
		if (_types.count() > 0):
		    aType = _types[0]
		    for w in v:
			words = models.Word.all().filter('word',w)
			if (words.count() == 0):
			    aWord = models.Word(word=w,word_type=aType)
			    aWord.save()
			    logging.debug('default.isWordz.5 :: Added word (%s) of type (%s)' % (w,aType.word_type))
	    words = models.Word.all()
	    status['words.2'] = words.count()
	    logging.debug('default.isWordz.6 :: words.count()=%s' % (words.count()))
            s_response = python_to_json(status)
        else:
            __error__ = 'INVALID Request.'
            data = {'success':False,'message':__error__}
            s_response = python_to_json(data)
        t = loader.get_template_from_string(__content__)
        c = {'content':s_response}
        content = t.render(Context(c,autoescape=False))
        return HttpResponse(content,mimetype=mimetype)
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        status = {'error':','.join(info_string.split('\n'))}
        s_response = python_to_json(status)
        return HttpResponse(s_response, mimetype=__mimetype)

