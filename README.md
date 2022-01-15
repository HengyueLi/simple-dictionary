# simple-dictionary
A super simplified dictionary (fundamental function and single-file script) that translates words from any language to any other language. 简易词典，从任意语言翻译成另一种语言。有道/沪江/...

一个超精简的在线词典。目标是快速识别语言然后翻译。输入过程尽量简单，功能尽量充足，词典库尽量多且可选。适用于多语言工作环境一个突如其来的陌生单词。

# 安装
一切从简，所有的内容都在一个`Python`脚本里面。直接下载`sd.py`就能用，另外也考虑编译成一些`bin`文件。

# 用法

## 基本用法 `sd xxx`
```
$ sd apple
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
## 打错建议
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
## 能识别语种
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
目前用的[第三方](https://translatedlabs.com/)在线识别，当出现网络问题(超时啥的)的时候用py库`langdetect`识别（错误率比较高）。

## 指定翻译方向
翻译方向表示位`A-B`,例如`ja-zh`表示从日语翻译成中文（`sd -c`打印出所有的语言码）。例如可以强制指明输入的是日文，需要翻译成中文：
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

## 同一个翻译方向可以内置多个词典
如下显示可用的词典
```
$ sd -l en-zh
┏━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ order ┃ direction ┃ dictionary  ┃ request URL                                          ┃
┡━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1     │ en->zh    │ 有道 英中   │ http://www.youdao.com/w/[WORD]%20/#keyfrom=dict2.top │
│ 2     │ en->zh    │ 沪江小D英中 │ https://dict.hjenglish.com/notfound/w/[WORD]         │
└───────┴───────────┴─────────────┴──────────────────────────────────────────────────────┘
```
可以切换不同的词典对比内容
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

## 使用代理
细节参考`sd -h`，可以设置好几条。在nat后面的网络这个还是很重要的（比如公司里）。
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

# 词典库
目标是添加各种各样的翻译方向，现在只有几种先用着，以后慢慢添加。`sd -l *`打印所有可用的词典。
目前只有
```
┏━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ order ┃ direction ┃ dictionary  ┃ request URL                                             ┃
┡━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1     │ zh->en    │ 有道 中英   │ http://www.youdao.com/w/eng/[WORD]/#keyfrom=dict2.index │
│ 2     │ zh->ja    │ 沪江小D中日 │ https://dict.hjenglish.com/notfound/jp/cj/[WORD]        │
│ 3     │ en->zh    │ 有道 英中   │ http://www.youdao.com/w/[WORD]%20/#keyfrom=dict2.top    │
│ 4     │ en->zh    │ 沪江小D英中 │ https://dict.hjenglish.com/notfound/w/[WORD]            │
│ 5     │ ja->zh    │ 沪江小D日中 │ https://dict.hjenglish.com/notfound/jp/jc/[WORD]        │
└───────┴───────────┴─────────────┴─────────────────────────────────────────────────────────┘
```

## 自己添加词典库
可以在issue留言，等不及了可以在源代码里面添加。需要会对`BeautifulSoup`懂一点。以下是"有道 中英"词典的例子。类的名字一定要用`DICTIONARY_`打头，用来扫描的。
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
