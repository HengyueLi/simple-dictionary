# simple-dictionary (sd)

A super simplified dictionary (fundamental function and single-file script) that translates words from any language to any other language. Aim to fast detect the input language and translate it. Keep the usage as simple as possible, as many functions as possible, as many dictionaries as possible. Network proxy is supported.

There are many projects that aim to wrap an online dictionary. Some of them are powerful dictionaries to translate a word from one language to another, but multiple languages are not supported. Some of them are not supporting user-defined dictionaries,... `sd` is aim to be a powerful dictionary with many functions. The translation, however, is kept as simple as possible.


# Install

## install packages
```
pip install requests bs4 html2text langdetect rich requests[socks]
```
or (better to do it in this way)
```
pip install -r requirements.txt
```

## install the script  
To keep every as simply as possible, everything is in a single `Python` script: `sd.py`. You can download it as use it directly. Compiling to `bin` file is also under consideration.

# Usage

## basic usage `sd xxx`
```
$ sd 苹果
┌─────────────────────────────┐
│ 苹果  zh-en   (沪江小D中英) │
├─────────────────────────────┤
│ ## 苹果                     │
│                             │
│ <píngguǒ>                   │
│                             │
│ apple                       │
│                             │
│                             │
└─────────────────────────────┘
```
## suggestion for mistaking
```
$ sd appl1
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ appl1  is not found by en-zh (有道 英中), suggestions:  ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ####  您要找的是不是:                                   │
│                                                         │
│ apply vt. 申请；涂，敷；应用 | vi. 申请；涂...          │
│                                                         │
│ apple n. 苹果；<俚>家伙                                 │
│                                                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```
## language detaction
```
$ sd 良し
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 良し  ja-zh   (沪江小D日中) ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ## 良し                     │
│                             │
│ <よし> <yoshi> ①            │
│                             │
│ ## 【名词】                 │
│                             │
│   * 1.好；行，可以。        │
│                             │
│                             │
└─────────────────────────────┘
```
The detection use a [3rd party online](https://translatedlabs.com/). If it is not success, timeout for instance, the local package `langdetect` is used. But this is not so accurate.

## set translation pair (IO-input)
A translation pair is represented as `A-B`, for example, `ja-zh` represents translating Japanese into Chinese (Print all language codes by `sd -c`). For example, the character of the word "Japan" in Chinese and Japanese are the same (日本), so one cannot tell which input language it is. We can clarify that we want to translate a word from Japanese to Chinese as:
```
$ sd  -i ja -o zh 日本
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 日本  ja-zh   (沪江小D日中) ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ## 日本                     │
│                             │
│ <にほん> <nihonn> ②         │
│                             │
│ ## 【名词】                 │
│                             │
│   * 1.日本。                │
│   * 2.同：日本（にっぽん）  │
│                             │
│                             │
└─────────────────────────────┘
```

## set default translation pairs
For one's own will, a preferred pair is used. For example, when an `en` word is detected, I want to translate it into `zh`. Then I need to set a pair `en->zh`. It is done by `sd  --config PREFER_TRANS_DIRECTION en zh`. By default, there are two pairs: `en->zh` and `zh->en`.


## set default language
- `default-in`: When the language of the input word is neither successfully detected nor clarified by the user, this setting will be used. Usually, you should set this value to the one that you frequently translate.
- `default-out`: When the language of the output word is not clarified by the user and the detected pair is not available currently, this setting will be used. Usually, you should set this value to your mother tongue.
- method to set:
  - example of setting `default-in` as `en`: `sd --config DEFAULT_LAN DEFAULT_LANG_IN en`
  - example of setting `default-out` as `zh`: `sd --config DEFAULT_LAN DEFAULT_LANG_OUT zh`



## Multiple dictionaries for one pair
For a given pair, list all available dictionaries by
```
$ sd -l en-zh
┏━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ order ┃ direction ┃ dictionary  ┃ request URL                                          ┃
┡━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1     │ en->zh    │ 有道 英中   │ http://www.youdao.com/w/[WORD]%20/#keyfrom=dict2.top │
│ 2     │ en->zh    │ 沪江小D英中 │ https://dict.hjenglish.com/notfound/w/[WORD]         │
└───────┴───────────┴─────────────┴──────────────────────────────────────────────────────┘
```
Fast to switch between dictionaries
```
$ sd apple -s 2
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ apple  en-zh   (沪江小D英中) ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ## apple                     │
│                              │
│ 英 <ˈæpəl> 美 <ˈæpəl>        │
│                              │
│ n.  苹果；苹果公司           │
│                              │
│                              │
└──────────────────────────────┘
```

## Proxy
Details can be found by `sd -h`. In the case of behind a NAT, employees in companies, for instance, this is very useful. An example is given below. Of cause, it is awkward if you type such as long command each time. You probably need to wrap a script by yourself. A configuration file is also under consideration...
```
sd -p http=socks5h://127.0.0.1:1080 apple
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ apple  en-zh   (有道 英中) ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 英 <ˈæp(ə)l> 美 <ˈæpl>     │
│                            │
│   * n. 苹果                │
│                            │
│ < 复数 apples >            │
│                            │
│                            │
└────────────────────────────┘
```
You can use many proxies:
`-p http=socks5h://127.0.0.1:1080@https=socks5h://127.0.0.1:1080`. The format of the proxy can be referred to the Python package `requests`.


# Available dictionaries
The final target of `sd` is to applicable for any translating pairs. For me, one `en`, `ja` and `zh` is used. I will try to append new pairs. Issue me if you has a request (better offer me a website meanwhile).  

（沪江词典需要用cookie，也看不懂里面有什么信息，安全起见我从[其他](https://github.com/Asutorufa/hujiang_dictionary)项目的代码里面copy过来的。）
```
┌───────┬───────────┬──────────────────────┬─────────────────────────────────────────────────────────┐
│ order │ direction │ dictionary           │ request URL                                             │
├───────┼───────────┼──────────────────────┼─────────────────────────────────────────────────────────┤
│ 1     │ zh->fr    │ 沪江小D中法          │ https://dict.hjenglish.com/fr/[WORD]                    │
│ 2     │ zh->de    │ www.godic.net zh->de │ https://www.godic.net/dicts/de/[WORD]                   │
│ 3     │ zh->ko    │ 沪江小D中韩          │ https://dict.hjenglish.com/kr/[WORD]                    │
│ 4     │ zh->en    │ 有道 中英            │ http://www.youdao.com/w/eng/[WORD]/#keyfrom=dict2.index │
│ 5     │ zh->en    │ 沪江小D中英          │ https://dict.hjenglish.com/notfound/w/[WORD]            │
│ 6     │ zh->ja    │ 沪江小D中日          │ https://dict.hjenglish.com/notfound/jp/cj/[WORD]        │
│ 7     │ en->zh    │ 有道 英中            │ http://www.youdao.com/w/[WORD]%20/#keyfrom=dict2.top    │
│ 8     │ en->zh    │ 沪江小D英中          │ https://dict.hjenglish.com/notfound/w/[WORD]            │
│ 9     │ en->ja    │ ejje.weblio E2J      │ https://ejje.weblio.jp/content/[WORD]                   │
│ 10    │ fr->zh    │ 沪江小D法中          │ https://dict.hjenglish.com/fr/[WORD]                    │
│ 11    │ de->zh    │ www.godic.net de->zh │ https://www.godic.net/dicts/de/[WORD]                   │
│ 12    │ ja->zh    │ 沪江小D日中          │ https://dict.hjenglish.com/notfound/jp/jc/[WORD]        │
│ 13    │ ko->zh    │ 沪江小D韩中          │ https://dict.hjenglish.com/kr/[WORD]                    │
└───────┴───────────┴──────────────────────┴─────────────────────────────────────────────────────────┘
```


## User defined dictionary
In principle, I can do it for you. One can issue a request. Or you can make one by yourself if you like. One needs to know a little about the `BeautifulSoup`. An example is shown below. One needs to define a class based on the father class `online_dictionary`. The name of the defined class must start with `DICTIONARY_`. The prefix is used for scanning the dictionary automatically.

```

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
```



# recover the default setting
`sd --reset`
