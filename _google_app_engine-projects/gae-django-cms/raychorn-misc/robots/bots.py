import re
import os, sys

import time
import zipfile

sys.path.insert(0,'z:\\python projects\\@lib')

from vyperlogix.misc import Args
from vyperlogix.js import minify
from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists
from vyperlogix.lists import ListWrapper

from django.utils import simplejson as jsonSerializer

normalize = lambda s:_utils.ascii_only(str(s))

__interested_in = 'robot-useragent'

__no_interest = []

__expected_keys = [
    'robot-id:',
    'robot-name:',
    'robot-cover-url:',
    'robot-details-url:',
    'robot-owner-name:',
    'robot-owner-url:',
    'robot-owner-email:',
    'robot-status:',
    'robot-purpose:',
    'robot-type:',
    'robot-platform:',
    'robot-availability:',
    'robot-exclusion:',
    'robot-exclusion-useragent:',
    'robot-noindex:',
    'robot-host:',
    'robot-from:',
    'robot-useragent:',
    'robot-language:',
    'robot-description:',
    'robot-history:',
    'robot-environment:',
    'modified-date:',
    'modified-by:'
]

__not_interested_in = ['???',"Due to a deficiency in Java it's not currently possible to set the User-Agent.","Due to a deficiency in Java it's not currently possible",'None','no','none','not available','yes','Road Runner: ImageScape Robot','logo.gif crawler']

__delimiters = [' libwww',' - ',',','http://',' | ',' at',' (','; ',' xxx','[','User-Agent: ','straight FLASH!! ','Road Runner: ',' G.R.A.B.','/xxxxxx','*.*',' JDK','v[','Mozilla/','x.xx','0.0',' v0.','.X','X.xx','x.x','x.y','vX','<version>','.x','{',"'",'n.','xxx','version#',' v','webs@recruit.co.jp','Nederland.zoek']

__corrections = {'Googlebot/2':'Googlebot/'}

__bots = []
__bots.append('ABCdatos BotLink/')
__bots.append('AlkalineBOT')
__bots.append('AnthillV')
__bots.append('appie/')
__bots.append('Arachnophilia')
__bots.append('Araneo/')
__bots.append('AraybOt/')
__bots.append('ArchitextSpider')
__bots.append('arks/')
__bots.append('ASpider/')
__bots.append('ATN_Worldwide')
__bots.append('Atomz/')
__bots.append('AURESYS/')
__bots.append('BackRub/')
__bots.append('BaySpider')
__bots.append('bbot/')
__bots.append('Big Brother')
__bots.append('Bjaaland/')
__bots.append('BlackWidow')
__bots.append('Die Blinde Kuh')
__bots.append('borg-bot/')
__bots.append('BoxSeaBot/')
__bots.append('BSpider/')
__bots.append('CACTVS Chemistry Spider')
__bots.append('Calif/')
__bots.append('Digimarc CGIReader/')
__bots.append('Checkbot/')
__bots.append('Spider')
__bots.append('CMC/')
__bots.append('combine/')
__bots.append('Confuzzledbot/')
__bots.append('CoolBot')
__bots.append('root/')
__bots.append('cosmos/')
__bots.append('Internet Cruiser Robot/')
__bots.append('Cusco/')
__bots.append('CyberSpyder/')
__bots.append('CydralSpider/')
__bots.append('DesertRealm.com')
__bots.append('Deweb/')
__bots.append('dienstspider/')
__bots.append('Digger/')
__bots.append('DIIbot')
__bots.append('grabber')
__bots.append('DNAbot/')
__bots.append('DragonBot/')
__bots.append('DWCP/')
__bots.append('LWP::')
__bots.append('EbiNess/')
__bots.append('EIT-Link-Verifier-Robot/')
__bots.append('elfinbot')
__bots.append('Emacs-w3/')
__bots.append('EMC Spider')
__bots.append('esculapio/')
__bots.append('esther')
__bots.append('Evliya Celebi')
__bots.append('explorersearch')
__bots.append('FastCrawler')
__bots.append('FelixIDE/')
__bots.append('Hazel')
__bots.append('ESIRover')
__bots.append('fido/')
__bots.append('Harvest/')
__bots.append('Hmhkki/')
__bots.append('KIT-Fireball/')
__bots.append('Fish-Search-Robot')
__bots.append('Robot du CRIM')
__bots.append('Freecrawl')
__bots.append('FunnelWeb')
__bots.append('gammaSpider')
__bots.append('gazz/')
__bots.append('gcreep/')
__bots.append('GetURL')
__bots.append('Golem/')
__bots.append('Googlebot/')
__bots.append('griffon/')
__bots.append('Gromit/')
__bots.append('Gulliver/')
__bots.append('Gulper Web Bot')
__bots.append('havIndex/')
__bots.append('AITCSRobot/')
__bots.append('Hometown Spider Pro')
__bots.append('wired-digital-newsbot/')
__bots.append('htdig/')
__bots.append('HTMLgobble')
__bots.append('iajaBot/')
__bots.append('IBM_Planetwide')
__bots.append('gestaltIconoclast/')
__bots.append('INGRID/')
__bots.append('IncyWincy/')
__bots.append('Informant')
__bots.append('InfoSeek Robot')
__bots.append('Infoseek Sidewinder')
__bots.append('InfoSpiders/')
__bots.append('inspectorwww/')
__bots.append('I Robot')
__bots.append('Iron33/')
__bots.append('IsraeliSearch/')
__bots.append('JavaBee')
__bots.append('JBot ')
__bots.append('JCrawler/')
__bots.append('JoBo ')
__bots.append('Jobot/')
__bots.append('JoeBot/')
__bots.append('JubiiRobot/')
__bots.append('jumpstation')
__bots.append('image.kapsi.net/')
__bots.append('Katipo/')
__bots.append('KDD-Explorer/')
__bots.append('KO_Yappo_Robot/')
__bots.append('LabelGrab/')
__bots.append('Linkidator/')
__bots.append('LinkScan Server/')
__bots.append('LinkWalker')
__bots.append('Lockon/')
__bots.append('Lycos/')
__bots.append('Magpie/')
__bots.append('marvin/infoseek')
__bots.append('MediaFox/')
__bots.append('MerzScope')
__bots.append('NEC-MeshExplorer')
__bots.append('MindCrawler')
__bots.append('UdmSearch')
__bots.append('moget/')
__bots.append('MOMspider/')
__bots.append('Monster/')
__bots.append('Motor/')
__bots.append('MSNBOT/')
__bots.append('Muninn/')
__bots.append('MuscatFerret/')
__bots.append('MwdSearch/')
__bots.append('NDSpider/')
__bots.append('NetCarta CyberPilot Pro')
__bots.append('NetMechanic')
__bots.append('NetScoop/')
__bots.append('newscan-online/')
__bots.append('NHSEWalker/')
__bots.append('Nomad-V2')
__bots.append('NorthStar')
__bots.append('ObjectsSearch/')
__bots.append('Occam/')
__bots.append('HKU WWW Robot')
__bots.append('OntoSpider/')
__bots.append('Openfind data gatherer')
__bots.append('Orbsearch/')
__bots.append('PackRat/')
__bots.append('PageBoy/')
__bots.append('ParaSite/')
__bots.append('Patric/')
__bots.append('web robot PEGASUS')
__bots.append('Peregrinator-Mathematics/')
__bots.append('PerlCrawler/')
__bots.append('Xavatoria/')
__bots.append('Duppies')
__bots.append('phpdig/')
__bots.append('PiltdownMan/')
__bots.append('Pioneer')
__bots.append('PortalJuice.com/')
__bots.append('PGP-KA/')
__bots.append('PlumtreeWebAccessor/')
__bots.append('Poppi/')
__bots.append('PortalBSpider/')
__bots.append('psbot/')
__bots.append('Raven-v2')
__bots.append('Resume Robot')
__bots.append('RHCS/')
__bots.append('RixBot')
__bots.append('Robbie/')
__bots.append('ComputingSite Robi/')
__bots.append('RoboCrawl')
__bots.append('Robofox')
__bots.append('Robozilla/')
__bots.append('Roverbot')
__bots.append('RuLeS/')
__bots.append('SafetyNet Robot')
__bots.append('Scooter/')
__bots.append('searchprocess/')
__bots.append('Senrigan')
__bots.append('SG-Scout')
__bots.append('Shagseeker')
__bots.append('SimBot/')
__bots.append('Site Valet')
__bots.append('SiteTech-Rover')
__bots.append('aWapClient')
__bots.append('SLCrawler')
__bots.append('Slurp/')
__bots.append('ESISmartSpider/')
__bots.append('Snooper/')
__bots.append('Solbot/')
__bots.append('LWP/')
__bots.append('Speedy Spider')
__bots.append('mouse.house/')
__bots.append('SpiderBot/')
__bots.append('spiderline/')
__bots.append('SpiderMan')
__bots.append('ssearcher100')
__bots.append('suke/')
__bots.append('suntek/')
__bots.append('Tarantula/')
__bots.append('tarspider')
__bots.append('dlw3robot/')
__bots.append('TechBOT')
__bots.append('Templeton/')
__bots.append('TitIn/')
__bots.append('TITAN/')
__bots.append('TLSpider/')
__bots.append('UCSD-Crawler')
__bots.append('UdmSearch/')
__bots.append('uptimebot')
__bots.append('urlck/')
__bots.append('URL Spider Pro')
__bots.append('Valkyrie/')
__bots.append('Verticrawlbot')
__bots.append('Victoria/')
__bots.append('vision-search/')
__bots.append('void-bot/')
__bots.append('Voyager/')
__bots.append('VWbot_K/')
__bots.append('w3index')
__bots.append('W3M2/')
__bots.append('CrawlPaper/')
__bots.append('WWWWanderer')
__bots.append('Spider/')
__bots.append('WebBandit/')
__bots.append('WebCatcher/')
__bots.append('WebCopy/')
__bots.append('WebFetcher/')
__bots.append('weblayers/')
__bots.append('WebLinker/')
__bots.append('WebMoose/')
__bots.append('WebQuest/')
__bots.append('Digimarc WebReader/')
__bots.append('WebReaper')
__bots.append('webvac/')
__bots.append('webwalk')
__bots.append('WebWalker/')
__bots.append('WebWatch')
__bots.append('Wget/')
__bots.append('whatUseek_winona/')
__bots.append('wlm-')
__bots.append('w3mir')
__bots.append('WOLP/')
__bots.append('WWWC/')
__bots.append('XGET/')

__source_fName = 'bots.txt'
__output_fName = os.path.splitext(__source_fName)[0]+'.json'
__output_agents_fName = os.path.splitext(__source_fName)[0]+('_%s.json'%(__interested_in))
__output_agents_list_fName = os.path.splitext(__source_fName)[0]+('_%s.txt'%(__interested_in))

_reParens = re.compile(r"\(.*?\)")

if (__name__ == '__main__'):
    print 'Reading from %s...' % (__source_fName)
    data = ListWrapper.ListWrapper(_utils.readFileFrom(__source_fName).split('\n'))
    m = len(data)
    record = {}
    records = []
    interested_in = {}
    iKey = 0
    last_key = ''
    fOut = open(__output_agents_list_fName,mode='w')
    i = 0
    while (i < m):
        try:
            item = data[i]
            print item
            if (len(item) > 0):
                toks = item.split(__expected_keys[iKey])
                if (len(toks) == 2):
                    last_key = __expected_keys[iKey].split(':')[0]
                    record[last_key] = normalize(toks[-1])
                    if (iKey+1 < len(__expected_keys)):
                        _toks = item.split(__expected_keys[iKey+1])
                        if (len(_toks) < 2):
                            while (len(_toks) < 2):
                                i += 1
                                item = data[i]
                                _toks = item.split(__expected_keys[iKey+1])
                                if (len(_toks) < 2):
                                    record[last_key] += normalize(item)
                                else:
                                    i -= 1
                                    iKey += 1
                                    break
                        else:
                            iKey += 1
                    else:
                        iKey = 0
            if (len(item) == 0):
                if (i+1 < m) and (len(data[i+1]) == 0) and (len(record.keys()) > 0):
                    i += 1
                    print '='*50
                    records.append(record)
                    k = record[__interested_in].strip()
                    if (len(k) > 0) and (k not in __not_interested_in):
                        results = _reParens.findall(k)
                        if (len(results) > 0):
                            for aResult in results:
                                k = k.replace(aResult,'')
                        if (len(k) > 0) and (k not in __not_interested_in):
                            for aDelimiter in __delimiters:
                                toks = k.split(aDelimiter)
                                if (len(toks) > 1):
                                    k = toks[0]
                            if (len(k) > 0) and (k not in __not_interested_in):
                                for aCorrectionK,aCorrectionV in __corrections.iteritems():
                                    k = k.replace(aCorrectionK,aCorrectionV)
                            if (len(k) > 0) and (k not in __not_interested_in):
                                isApproved = False
                                approvedBot = ''
                                for aBot in __bots:
                                    if (k.find(aBot) > -1):
                                        isApproved = True
                                        approvedBot = aBot
                                        break
                                if (isApproved) and (len(approvedBot) > 0):
                                    record[__interested_in] = approvedBot
                                    if (not interested_in.has_key(approvedBot)):
                                        for k,v in record.iteritems():
                                            if (v.find('"') > -1):
                                                record[k] = v.replace('"','').strip()
                                        for item in __no_interest:
                                            del record[item]
                                        interested_in[approvedBot] = record
                                        print >> fOut, approvedBot
                    record = {}
            i += 1
        except:
            pass
    fOut.flush()
    fOut.close()
    try:
        json = jsonSerializer.dumps(records)
        print 'Writing to %s...' % (__output_fName)
        _utils.writeFileFrom(__output_fName,json)
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        print info_string
        
        for n in xrange(0,len(records)+1):
            try:
                json = jsonSerializer.dumps(records[n])
            except Exception, e:
                info_string = _utils.formattedException(details=e)
                print info_string
    try:
        json = jsonSerializer.dumps(interested_in)
        print 'Writing to %s...' % (__output_agents_fName)
        _utils.writeFileFrom(__output_agents_fName,json)
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        print info_string
    print 'Verification...'
    json = _utils.readFileFrom(__output_agents_fName)
    iData = jsonSerializer.loads(json)
    keys1 = interested_in.keys()
    keys2 = iData.keys()
    keysDiff = list(set(keys1) - set(keys2))
    assert len(keysDiff) == 0, 'Oops, something went wrong. Better check your logic...'
    print 'Done !'
    