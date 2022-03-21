#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# Description:
#          an online dictionary. More details see by option -h
#
#──────────────────────────
# Author:  hengyueli@gamil.com
#──────────────────────────
#  update:
#       2022.01.17
#       2022.01.07  rebuild from the old script
#──────────────────────────
# used:
import os
import json
import sys
import inspect
import argparse
import logging
import requests
import configparser

#
import bs4
import html2text
import langdetect
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
import rich
#──────────────────────────
#══════════════════════════════════════════════════════════════════════════════════════════════════════════════════














class config():

    @staticmethod
    def getConfigFileName():
        return 'sd_config.ini'

    @staticmethod
    def getConfigFileLocationDir():
        return os.path.join(os.path.expanduser('~'), '.config' )

    @staticmethod
    def default_configuration():
        return {
            'DEFAULT_LAN':{
                #  default translation direction, try the input language in DEFAULT_LANG_IN and output is  DEFAULT_LANG_OUT
                'DEFAULT_LANG_IN':'en',
                'DEFAULT_LANG_OUT':'zh',
            },
            "PREFER_TRANS_DIRECTION":{
                # According to the detected (or input) language, a more preferd translation is used.
                # The key and the value are correcsponding to the input and output language
                # For example:
                #    if the input is detected as 'en', personaly I would like to translate it into 'zh'.
                #    Likewise, when the input is 'zh', I like to translate it into 'en'.
                #    In this case, the configuration should be
                #    PREFER_TRANS_DIRECTION = { "en":"zh", "zh":"en"  }
                # This has higher priority to DEFAULT_LANG_OUT, but lower than the args input.
                "en":'zh',
                'zh':'en',
            },
            "CONFIG":{
                "USE_CACHE":False,
            }
        }

    @classmethod
    def getConfigFilePath(cls):
        return os.path.join( cls.getConfigFileLocationDir() ,  cls.getConfigFileName()  )

    @classmethod
    def getConfigDict(cls):
        configFile = cls.getConfigFilePath()
        if not os.path.exists(configFile):
            logging.debug("no config file, use default settings")
            r= cls.default_configuration()
        else:
            logging.debug("use config file: {}".format(configFile))
            parser = configparser.ConfigParser()
            parser.optionxform = str
            parser.read(configFile)
            r= {s:dict(parser.items(s)) for s in parser.sections()}
        logging.debug("configuration = {}".format(str(r)))
        return r

    @classmethod
    def setConfigDict(cls,Dict):
        configDir = cls.getConfigFileLocationDir()
        configFile = cls.getConfigFilePath()
        if not os.path.exists(configDir):
            os.makedirs(configDir)
        parser = configparser.ConfigParser()
        parser.optionxform = str
        for section in Dict:
            parser.add_section(section)
            for k in Dict[section]:
                parser.set(section, k, Dict[section][k] )
        with open(configFile, 'w') as f:
            parser.write(f)



class Cache():

    def __init__(self):
        self.Dict = None

    @staticmethod
    def __getCacheFileName():
        return 'sd_cache.json'

    @staticmethod
    def __getConfigFileLocationDir():
        return os.path.join(os.path.expanduser('~'), '.config' )

    def __getCacheFilePath(self):
        return os.path.join(self.__getConfigFileLocationDir() , self.__getCacheFileName() )

    def __getCacheDict(self):
        if not os.path.exists(self.__getCacheFilePath()):
            try:
                os.mkdirs(self.__getConfigFileLocationDir())
            except:
                pass
            return {}
        else:
            with open(self.__getCacheFilePath(),'r') as f:
                return json.loads(f.read())


    def get(self,dictionaryName,key):
        cache = self.__getCacheDict()
        d = cache.get(dictionaryName,None)
        if d is None:
            return None,None
        return d.get(key,(None,None))

    def set(self,dictionaryName,key,val):
        cache = self.__getCacheDict()
        if dictionaryName not in cache:
            cache[dictionaryName] = {}
        cache[dictionaryName][key] = val
        with open(self.__getCacheFilePath(),'w') as f:
            f.write( json.dumps(cache) )


class Requests():

    def __init__(self,**reqkwargs):
        self.reqkwargs = reqkwargs

    def get(self,url,para={}):
        para1 = dict(self.reqkwargs)
        para2 = dict(para)
        # para1 is passed from main, should be first priority?
        for k in para1:
            if k in para2:
                logging.warning("setRequestPara has setting {}={} which conflict to main setting {}={}, and will be ignored ".format(k,para2[k],k,para1[k]))
            para2[k] = para1[k]

        if 'headers' not in para2:
            para2['headers'] = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        logging.debug("request.get = [{}]".format(url))
        return requests.get(url,**para2)

    def GetSoup(self,url,para={}):
        r = self.get(url,para=para)
        return bs4.BeautifulSoup(r.content, 'html.parser')

    def post(self,url,data={}):
        return requests.post(url,data=data,**self.reqkwargs)

    def postJson(self,url,data={}):
        return self.post(url,data).json()



class online_dictionary():

    #------------------------------------------
    @staticmethod
    def selectionWeight() -> int: return 1

    @staticmethod
    def getDictionaryName()->str:return "NOT SET"

    @staticmethod
    def getTranslationDirection() -> list:pass

    @staticmethod
    def makeURL(word)->str:pass

    @staticmethod
    def IsExists(soup):pass

    @staticmethod
    def getHTMLfromSoup_translation(soup)->str:pass

    @staticmethod
    def getHTMLfromSoup_suggestion(soup)->str:pass

    @staticmethod
    def setRequestPara()->dict:return {}

    #------------------------------------------

    def __init__(self,ReqObj,Config=None):
        self.ReqObj = ReqObj
        self.Config = Config

    def __isUseCache(self):
        if self.Config is not None:
            return self.Config['USE_CACHE']
        else:
            return False


    def GetHTMLtoplainText(self,HTMLstring):
        h = html2text.HTML2Text()
        h.ignore_links = True
        # h.ignore_images = True
        return h.handle (HTMLstring)
        # return html2text.html2text(HTMLstring)

    def getByRequest(self,word):
        soup = self.ReqObj.GetSoup( self.makeURL(word), para= self.setRequestPara())
        if self.IsExists(soup):
            logging.debug("translation is found")
            html = self.getHTMLfromSoup_translation(soup)
            ConsolePrintTxt = self.GetHTMLtoplainText(html)
            return True,ConsolePrintTxt
        else:
            logging.debug("translation is not found, get suggestions")
            html = self.getHTMLfromSoup_suggestion(soup)
            ConsolePrintTxt = self.GetHTMLtoplainText(html)
            return False,ConsolePrintTxt

    def PrintTranslation(self,word):
        isUseCache = self.__isUseCache()
        logging.debug('use cache = [{}]'.format(isUseCache))
        if isUseCache:
            cache = Cache()
            cg = cache.get(dictionaryName=self.getDictionaryName(),key=word)
            if cg is None:
                isExist,ConsolePrintTxt = cg
            else:
                isExist,ConsolePrintTxt = self.getByRequest(word=word)
                cache.set(dictionaryName=self.getDictionaryName(),key=word,val=[isExist,ConsolePrintTxt])
        else:
            isExist,ConsolePrintTxt = self.getByRequest(word=word)
        #-----
        console = Console()
        table = rich.table.Table()
        FROM,TO = self.getTranslationDirection()
        if isExist:
            table.add_column( "[yellow]{}[/yellow]".format(word) + "  [green]{}-{}[/green]   [green]({})[/green]".format(FROM,TO,self.getDictionaryName()))
        else:
            table.add_column( "[red]{}[/red]".format(word) + "  is not found by [red]{}-{}[/red] ({}), suggestions: ".format(FROM,TO,self.getDictionaryName()))
        table.add_row(ConsolePrintTxt.replace('[',"<").replace(']',">"))
        console.print(table)


    # def PrintTranslation(self,word):
    #     console = Console()
    #     table = rich.table.Table()
    #     soup = self.ReqObj.GetSoup( self.makeURL(word), para= self.setRequestPara())
    #     FROM,TO = self.getTranslationDirection()
    #     if self.IsExists(soup):
    #         logging.debug("translation is found")
    #         html = self.getHTMLfromSoup_translation(soup)
    #         ConsolePrintTxt = self.GetHTMLtoplainText(html)
    #         table.add_column( "[yellow]{}[/yellow]".format(word) + "  [green]{}-{}[/green]   [green]({})[/green]".format(FROM,TO,self.getDictionaryName()))
    #     else:
    #         logging.debug("translation is not found, get suggestions")
    #         html = self.getHTMLfromSoup_suggestion(soup)
    #         ConsolePrintTxt = self.GetHTMLtoplainText(html)
    #         table.add_column( "[red]{}[/red]".format(word) + "  is not found by [red]{}-{}[/red] ({}), suggestions: ".format(FROM,TO,self.getDictionaryName()))
    #     table.add_row(ConsolePrintTxt.replace('[',"<").replace(']',">"))
    #     console.print(table)







#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#                          dictionary
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





class DICTIONARY_EnglishToChinese1(online_dictionary):

    @staticmethod
    def selectionWeight() -> int: return 5

    @staticmethod
    def getDictionaryName()->str:
        return "有道 英中"

    @staticmethod
    def getTranslationDirection() -> list:
        return ['en','zh']

    @staticmethod
    def makeURL(word)->str:
        return "http://www.youdao.com/w/{}%20/#keyfrom=dict2.top".format(word)

    @staticmethod
    def IsExists(soup):
        pronounces = soup.find_all("div", {"class": "baav"})
        return len(pronounces) != 0

    @staticmethod
    def getHTMLfromSoup_translation(soup)->str:
        if soup == None: soup = self.soup
        pronounces = soup.find_all("div", {"class": "baav"})[0]
        trans  = soup.find_all("div", {"class": "trans-container"})[0]
        return str(pronounces)+str(trans)

    @staticmethod
    def getHTMLfromSoup_suggestion(soup)->str:
        suggestion = soup.find_all("div", {"class": "error-typo"})
        if len(suggestion) == 0: return ' None '
        suggestion = suggestion[0]
        for a in suggestion.findAll('a'):
            del a['href']
        return str(suggestion)
    #------------------------------------------



class DICTIONARY_ChineseToEnglish1(online_dictionary):

    @staticmethod
    def getDictionaryName()->str:
        return "有道 中英"

    @staticmethod
    def getTranslationDirection() -> list:
        return ['zh','en']

    @staticmethod
    def makeURL(word)->str:
        return "http://www.youdao.com/w/eng/{}/#keyfrom=dict2.index".format(word)

    @staticmethod
    def IsExists(soup):
        trans = soup.find_all("div", {"id": "phrsListTab"})
        return len(trans) != 0

    @staticmethod
    def getHTMLfromSoup_translation(soup)->str:
        pronounces = ' '
        trans  = soup.find_all("p", {"class": "wordGroup"})[0]
        for a in trans.findAll('a'):
            del a['href']
        return str(  trans  )

    @staticmethod
    def getHTMLfromSoup_suggestion(soup)->str:
        suggestion = soup.find_all("div", {"id": "rel-search"})
        if len(suggestion) == 0: return ' None '
        suggestion = suggestion[0]
        for a in suggestion.findAll('a'):
            del a['href']
        return str(suggestion)







class HuJiang_online(online_dictionary):

    @staticmethod
    def setRequestPara()->dict:
        # cookie is copied from https://github.com/Asutorufa/hujiang_dictionary
        return {'headers':{
            'cookie': 'HJ_UID=0f406091-be97-6b64-f1fc-f7b2470883e9; HJ_CST=1; HJ_CSST_3=1;TRACKSITEMAP=3%2C; HJ_SID=393c85c7-abac-f408-6a32-a1f125d7e8c6; _REF=; HJ_SSID_3=4a460f19-c0ae-12a7-8e86-6e360f69ec9b; _SREF_3=; HJ_CMATCH=1',
        }}

    @staticmethod
    def IsExists(soup):
        div = soup.find('header',{'class':'word-details-pane-header'})
        return div is not None


    @staticmethod
    def getHTMLfromSoup_translation(soup)->str:
        header = soup.find('header',{'class':'word-details-pane-header'})
        return str(header)


    @staticmethod
    def getHTMLfromSoup_suggestion(soup)->str:
        ul = soup.find('div',{'class':'word-suggestions'})
        # print(soup)
        return str(ul)


class DICTIONARY_JapaneseToChinese1(HuJiang_online):

    @staticmethod
    def getDictionaryName()->str:
        return "沪江小D日中"

    @staticmethod
    def getTranslationDirection() -> list:
        return ['ja','zh']

    @staticmethod
    def makeURL(word)->str:
        url = "https://dict.hjenglish.com/notfound/jp/jc/{}".format(word)
        return url

class DICTIONARY_ChineseToJapanese1(HuJiang_online):

    @staticmethod
    def getDictionaryName()->str:
        return "沪江小D中日"

    @staticmethod
    def getTranslationDirection() -> list:
        return ['zh','ja']

    @staticmethod
    def makeURL(word)->str:
        url = "https://dict.hjenglish.com/notfound/jp/cj/{}".format(word)
        return url

class DICTIONARY_EnglishToChinese_hujiang(HuJiang_online):

    @staticmethod
    def selectionWeight() -> int: return 1

    @staticmethod
    def getDictionaryName()->str:
        return "沪江小D英中"

    @staticmethod
    def getTranslationDirection() -> list:
        return ['en','zh']

    @staticmethod
    def makeURL(word)->str:
        url = "https://dict.hjenglish.com/notfound/w/{}".format(word)
        return url

class DICTIONARY_ChineseToEnglish_hujiang(DICTIONARY_EnglishToChinese_hujiang):

    @staticmethod
    def selectionWeight() -> int: return 2

    @staticmethod
    def getDictionaryName()->str:
        return "沪江小D中英"

    @staticmethod
    def getTranslationDirection() -> list:
        return ['zh','en']

class DICTIONARY_Korean2Chinese_hujiang(HuJiang_online):

    @staticmethod
    def getDictionaryName()->str:
        return "沪江小D韩中"

    @staticmethod
    def getTranslationDirection() -> list:
        return ['ko','zh']

    @staticmethod
    def makeURL(word)->str:
        url = "https://dict.hjenglish.com/kr/{}".format(word)
        return url

class DICTIONARY_Chinese2Korean_hujiang(DICTIONARY_Korean2Chinese_hujiang):

    @staticmethod
    def getDictionaryName()->str:
        return "沪江小D中韩"

    @staticmethod
    def getTranslationDirection() -> list:
        return ['zh','ko']

    @staticmethod
    def makeURL(word)->str:
        url = "https://dict.hjenglish.com/kr/{}".format(word)
        return url

class DICTIONARY_French2Chinese_hujiang(HuJiang_online):

    @staticmethod
    def getDictionaryName()->str:
        return "沪江小D法中"

    @staticmethod
    def getTranslationDirection() -> list:
        return ['fr','zh']

    @staticmethod
    def makeURL(word)->str:
        url = "https://dict.hjenglish.com/fr/{}".format(word)
        return url


class DICTIONARY_Chinese2French_hujiang(DICTIONARY_French2Chinese_hujiang):

    @staticmethod
    def getDictionaryName()->str:
        return "沪江小D中法"

    @staticmethod
    def getTranslationDirection() -> list:
        return ['zh','fr']

    @staticmethod
    def makeURL(word)->str:
        url = "https://dict.hjenglish.com/fr/{}".format(word)
        return url





class DICTIONARY_EnglishToJapanese1(online_dictionary):

    @staticmethod
    def getDictionaryName()->str:
        return "ejje.weblio E2J"

    @staticmethod
    def getTranslationDirection() -> list:
        return ['en','ja']

    @staticmethod
    def makeURL(word)->str:
        return "https://ejje.weblio.jp/content/{}".format(word)

    @staticmethod
    def IsExists(soup):
        return len(soup.select('div.summaryM.descriptionWrp')) >0


    @staticmethod
    def getHTMLfromSoup_translation(soup)->str:
        return str(  soup.select('div.summaryM.descriptionWrp')[0] )

    @staticmethod
    def getHTMLfromSoup_suggestion(soup)->str:
        suggestion = soup.find('div',{'class':'spellCheck'})

        return str(suggestion)








class DICTIONARY_German2Chinese(online_dictionary):

    @staticmethod
    def getDictionaryName()->str:
        return "www.godic.net de->zh"

    @staticmethod
    def getTranslationDirection() -> list:
        return ['de','zh']

    @staticmethod
    def makeURL(word)->str:
        return "https://www.godic.net/dicts/de/{}".format(word)

    @staticmethod
    def IsExists(soup):
        return soup.find('div',{'id':'ExpFC',"class":'explain_wrap'}) is not None


    @staticmethod
    def getHTMLfromSoup_translation(soup)->str:
        div = soup.find('div',{'id':'ExpFC',"class":'explain_wrap'})
        div.find('a').decompose()
        div.find('div',{'class':'thumbnialNeedUpload'}).decompose()
        return str(div)

    @staticmethod
    def getHTMLfromSoup_suggestion(soup)->str:
        suggestion = soup.find('div',{"class":'suggestion-list'})
        return str(suggestion)

class DICTIONARY_Chinese2German(DICTIONARY_German2Chinese):

    @staticmethod
    def getDictionaryName()->str:
        return "www.godic.net zh->de"

    @staticmethod
    def getTranslationDirection() -> list:
        return ['zh','de']










# class languageDetection_langdetect():
#
#     @staticmethod
#     def detect(cls,word):
#         g = langdetect.detect_langs(word)[0]
#         logging.debug('word [{}] is detected as {} with P={}, use lib langdetect'.format(word,g.lang,g.prob))
#         return g.lang[0:2]
#
# class languageDetection_langdetect():



class languageDetection():


    def __init__(self,reqObj):
        self.reqObj = reqObj

    @staticmethod
    def getTable631():
        # not all of them, details see https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
        return {'af': 'afrikaans', 'ar': 'arabic', 'bg': 'bulgarian', 'bn': 'bengali',
                'ca': 'catalan', 'cs': 'czech', 'cy': 'welsh', 'da': 'danish', 'de': 'german',
                'el': 'greek', 'en': 'english', 'es': 'spanish', 'et': 'estonian', 'fa': 'persian',
                'fi': 'finnish', 'fr': 'french', 'gu': 'gujarati', 'he': 'hebrew', 'hi': 'hindi',
                'hr': 'croatian', 'hu': 'hungarian', 'id': 'indonesian', 'it': 'italian', 'ja': 'japanese',
                'kn': 'kannada', 'ko': 'korean', 'lt': 'lithuanian', 'lv': 'latvian', 'mk': 'macedonian',
                'ml': 'malayalam', 'mr': 'marathi', 'ne': 'nepali', 'nl': 'dutch', 'no': 'norwegian',
                'pa': 'punjabi', 'pl': 'polish', 'pt': 'portuguese', 'ro': 'romanian', 'ru': 'russian',
                'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'sq': 'albanian', 'sv': 'swedish',
                'sw': 'swahili', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tl': 'tagalog',
                'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu', 'vi': 'vietnamese', 'zh': 'chinese'}


    @staticmethod
    def detect_langdetect(word):
        g = langdetect.detect_langs(word)[0]
        # g.prob
        logging.debug('word [{}] is detected as {} with P={}, use lib langdetect'.format(word,g.lang,g.prob))
        return g.lang[0:2]

    def detect_translatedlabs(self,word):
        logging.debug("detect '{}' by translatedlabs".format(word))
        url = 'https://api.translatedlabs.com/language-identifier/identify'
        data = '{{"text":"{}","uiLanguage":"en","etnologue":true}}'.format(word).encode()
        language = self.reqObj.postJson(url,data=data)['language'].lower()
        table = self.getTable631()
        for code in table:
            if table[code] == language:
                return code
        logging.debug("can not find language '{}' in table631".format(language))
        return "??"

    # more api
    #  https://languagetool.org/


    def detect(self,word):
        try:
            return self.detect_translatedlabs(word)
        except:
            return self.detect_langdetect(word)







# config.getConfigDict()[]

class selectDictionary():

    # DEFAULT_LANG_IN = DEFAULT_LANG_IN
    # DEFAULT_LANG_OUT = DEFAULT_LANG_OUT
    # PREFER_TRANS_DIRECTION = PREFER_TRANS_DIRECTION

    def __init__(self,reqObj=None,select=1):
        if reqObj is None:
            self.reqObj = Requests()
        self.reqObj = reqObj
        self.select = select
        self.Config = config.getConfigDict()
        # self.Config['PREFER_TRANS_DIRECTION']

    @property
    def PREFER_TRANS_DIRECTION(self):
        return self.Config['PREFER_TRANS_DIRECTION']
    @property
    def DEFAULT_LANG_IN(self):
        return self.Config['DEFAULT_LAN']['DEFAULT_LANG_IN']
    @property
    def DEFAULT_LANG_OUT(self):
        return self.Config['DEFAULT_LAN']['DEFAULT_LANG_OUT']


    @staticmethod
    def scan_dictionaries():
        dictionaries = {}
        for name, cls in inspect.getmembers(sys.modules[__name__]):
            if "DICTIONARY_" == name[:11]:
                key = '-'.join(cls.getTranslationDirection())
                if key not in dictionaries:
                    dictionaries[key] = []
                dictionaries[key].append(cls)
        return dictionaries

    def languageDetection(self,word):
        return languageDetection(self.reqObj).detect(word)

    @classmethod
    def select_dictionaries(cls,transDirect,dictionaries=None)->list:
        if dictionaries is None:
            dictionaries = cls.scan_dictionaries()
        if transDirect == "*":
            # return all
            r = []
            for t in dictionaries:
                r +=  dictionaries[t]
            return r
        if transDirect not in dictionaries:
            logging.debug("no dictionary for {}".format(transDirect))
            return []
        else:
            dList = list(dictionaries[transDirect])
            dList = sorted(dList,key= lambda item: item.selectionWeight(),reverse=True)
            return dList

    def selectDictFromDictList(self,tranDirect,dictionaries):
        dList = self.select_dictionaries(transDirect=tranDirect,dictionaries=dictionaries)
        if len(dList) == 0:
            return None
        logging.debug("{} optional dictionaries for {} can be found, they are: {}".format( len(dictionaries[tranDirect]),tranDirect, ",".join([d.getDictionaryName() for d in dictionaries[tranDirect]]) ))
        if 0< self.select <=len(dList):
            logging.debug("select dictionary = {} according to the weight".format(dList[self.select-1].getDictionaryName()))
            return dList[self.select-1]
        else:
            logging.error("select = {} is out of range. You only have {} directionaries for {}".format(self.select,len(dList),tranDirect))
            logging.info("reset select = 1")
            return dList[0]

    def select_case_EE(cls,dictionaries,word):
        logging.debug("select dictionary: case EE")
        I = cls.languageDetection(word)
        if I in cls.PREFER_TRANS_DIRECTION:
            O = cls.PREFER_TRANS_DIRECTION[I]
            logging.debug("I={} is in the preferd list, set O as {}".format(I,O))
        else:
            O = cls.DEFAULT_LANG_OUT
            logging.debug("I={} is not in the preferd list, set O as default: {}".format(I,O))
        transDirect = I+"-"+O
        dic = cls.selectDictFromDictList(transDirect,dictionaries)
        if dic is None:
            I = cls.DEFAULT_LANG_IN
            logging.debug("reset I as default: {}".format(I))
            return cls.select_case_IE(dictionaries,word,I)
        else:
            return dic,transDirect
    def select_case_EO(cls,dictionaries,word,O):
        logging.debug("select dictionary: case EO")
        I = cls.languageDetection(word)
        transDirect = I+"-"+O
        dic = cls.selectDictFromDictList(transDirect,dictionaries)
        if dic is None:
            transDirect = cls.DEFAULT_LANG_IN + "-"+O
            return cls.select_case_IO(dictionaries,word,I,O)
        else:
            return dic,transDirect
    def select_case_IE(cls,dictionaries,word,I):
        logging.debug("select dictionary: case IE")
        if I in cls.PREFER_TRANS_DIRECTION:
            O = cls.PREFER_TRANS_DIRECTION[I]
            logging.debug("I={} is in preferd list, set O as {}".format(I,O))
            transDirect = I + "-"+O
            dic = cls.selectDictFromDictList(transDirect,dictionaries)
            if dic is not None:
                return dic,transDirect
        O = cls.DEFAULT_LANG_OUT
        return cls.select_case_IO(dictionaries,word,I,O)
    def select_case_IO(cls,dictionaries,word,I,O):
        logging.debug("select dictionary: case IO")
        transDirect = I + "-"+O
        dic = cls.selectDictFromDictList(transDirect,dictionaries)
        return dic,transDirect

    def selectdict(cls,word,langIn,langOut):
        #
        #   Priorities of tanslations in 4 cases: E-E,E-O,I-E,I-O.
        #   For example, I-E represents the input language is given while the Output language is missing.
        #
        #      E-E                                 E-O                              I-E                         I-O
        #       ↓                                   ↓                                ↓                           ↓
        #     detect I                           detect I                        preferd O exist?             IO available?
        #       ↓                                   ↓                            ↓yes        ↓no              ↓yes      ↓no
        #  set preferd O if exist,              available?                   IO available?   ↓              selected    error
        #  else set default O                  ↓yes     ↓no                  ↓yes     no→ set default O
        #       ↓                           selected    set default I      selected          ↓
        #   IO available?                               ↓                                 to case I-O
        #    ↓yes       ↓no                             to case I-O
        #   selected   set default I
        #               ↓
        #             to case I-E
        dictionaries = cls.scan_dictionaries()
        if langIn is None:
            if langOut is None:
                return cls.select_case_EE(dictionaries,word)
            else:
                return cls.select_case_EO(dictionaries,word,langOut)
        else:
            if langOut is None:
                return cls.select_case_IE(dictionaries,word,langIn)
            else:
                return cls.select_case_IO(dictionaries,word,langIn,langOut)













if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
    description='''
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ Super-simplified dictionary for translations from ┃
        ┃ any language into another.                        ┃
        ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    ''')
    # parser.add_argument('Input', type=str, nargs='+', help='input words')
    parser.add_argument('Input', type=str, nargs='*', help='input words')
    parser.add_argument('-p','--proxy',help='<key1>=<value1>;<key2>=<value2>;...see proxies in lib requests',required=False,)
    parser.add_argument('-i','--inputlanguage',help='specify the input language: en, ja, zh',required=False,)
    parser.add_argument('-o','--outputlanguage',help='specify the output language: en, ja, zh',required=False)
    parser.add_argument('-d','--debug',help='debug',required=False,action="store_true")
    parser.add_argument('-c','--code',help='print language codes: en, ja, zh,...',required=False,action="store_true")
    parser.add_argument('-s','--select',help='If multiple dictionary are available, select one according to the related-weight, default is 1 (the first one). Should be a non-zero integer',type=int,default=1,required=False)
    parser.add_argument('-l','--list', nargs='?',help='list all available dictionaries for a given translation-direction, for example -l zh-en',type=str,const="*",required=False)
    parser.add_argument('-C','--config',help="set config file. Format --config section key value",nargs='*',required=False)
    parser.add_argument('-r','--reset',help="delete config file. All setting by default",required=False,action="store_true")

    args = vars(parser.parse_args())
    # print(args)

    console = Console()


    #>>>>>>> set log >>>>>>>>>>>>>>>>>>>
    if args['debug']:
        level = logging.DEBUG
    else:
        level = logging.INFO
    root = logging.getLogger()
    root.setLevel(   level  )
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(  level  )
    handler.setFormatter( logging.Formatter('%(asctime)s %(levelname)s %(message)s')   )
    root.addHandler(handler)



    if args['code']:
        table631 = languageDetection.getTable631()
        user_renderables = [Panel( "[green]{}[/green]".format(c) + '\n' + "[#F47983]{}[/#F47983]".format(table631[c])   , expand=True) for c in table631]
        console.print(Columns(user_renderables))
        sys.exit()

    if args['list']:
        from rich.table import Table
        transDirect = args['list']
        #-----
        # validation
        if transDirect != "*":
            if '-' not in transDirect:
                console.print("transDirect format error, example: zh-en")
                sys.exit()
            I,O = transDirect.split('-')
            table631 = languageDetection.getTable631()
            if not (I in table631 and O in table631):
                console.print("[green]in[/green]/[#F47983]out[/#F47983] language code [green]{}[/green]/[#F47983]{}[/#F47983] is not a 631 code or not included in table, use -c to list avalable codes".format(I,O))
                sys.exit()
        #-----
        dList = selectDictionary.select_dictionaries(transDirect)

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("order")
        table.add_column("direction")
        table.add_column("dictionary", style="dim")
        table.add_column("request URL", style="dim")
        for i,d in enumerate(dList):
            table.add_row( str(i+1), "{}->{}".format(*d.getTranslationDirection())  , "[green]"+d.getDictionaryName()+"[/green]", d.makeURL("[WORD]") )
        console.print(table)
        sys.exit()

    if args['reset']:
        configFilePath = config.getConfigFilePath()
        if os.path.exists(configFilePath):
            os.remove(configFilePath)
        sys.exit()

    if args['config']:
        opt = args['config']
        if len(opt) != 3:
            console.print("need exact 3 args: section-name key-name value")
            sys.exit()
        con_dict = config.getConfigDict()
        con_dict[opt[0]][opt[1]] = opt[2]
        config.setConfigDict(con_dict)
        sys.exit()






    if len(args['Input'])==0:
        logging.error("empy input")
        os.system( " {} {} -h ".format(sys.executable,os.path.abspath(__file__)) )
        sys.exit()





    if args['proxy'] is None:
        ReqObj = Requests()
    else:
        proxies = {}
        pairs = args['proxy'].split("@")
        for kv in pairs:
            k,v = kv.split("=")
            proxies[k]=v
        ReqObj = Requests(proxies=proxies)
        logging.debug("use proxy {}".format(proxies))

    word_trans = " ".join([ w.strip() for w in args['Input']])

    dictionary,transDirect = selectDictionary(ReqObj,select=args['select']).selectdict( word= word_trans,langIn=args['inputlanguage'],langOut=args['outputlanguage'])

    if dictionary is None:
        logging.error("No available dictionary for [{}] ({}), use --debug to see the details".format( " ".join(args['Input']), transDirect ))
    else:
        d = dictionary(ReqObj,Config=config.getConfigDict()['CONFIG'])
        d.PrintTranslation( word_trans )
