# simple-dictionary (sd)

# [ENGLISH README](https://github.com/HengyueLi/simple-dictionary/blob/main/README_ENG.md)

一个超精简的在线词典。目标是快速识别语言然后翻译。输入过程尽量简单，功能尽量充足，词典库尽量多且可选。有代理功能。

在网上找到要么就是有道，要么就是沪江，要么只有英文，内容详细但是功能太少。`sd`力求功能多一点，内容简单一点。

# 安装

## 安装依赖
```
pip install requests bs4 html2text langdetect rich requests[socks]
```
或者(最好)
```
pip install -r requirements.txt
```

## 安装脚本
一切从简，所有的内容都在一个`Python`脚本里面。直接下载`sd.py`就能用。比如我直接改名叫`sd`就用着了。另外也在考虑编译成一些`bin`文件,还有Cython加速啥的，再说吧。

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

## 指定翻译方向(IO-input)
翻译方向表示为`A-B`,例如`ja-zh`表示从日语翻译成中文（`sd -c`打印出所有的语言码）。例如可以强制指明输入的是日文，需要翻译成中文：
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

## 设置默认翻译方向(preferred-trans)
当没有输入翻译方向时，使用默认设置。比如当检测输入为`en`（英文）时，默认翻译成`zh`（中文）则需要增加一条方向为`en->zh`。设置方法是`sd  --config PREFER_TRANS_DIRECTION en zh`。
当前默认设置两条为：`en->zh`,`zh->en`

## 设置默认语言
- `default-in`: 当输入单词既没有人为指定语种，也没有成功被识别时，使用`default-in`指定的语言。通常设置成常用的查询语种。
- `default-out`: 当没有人为指定翻译方向的目标语种或者通过默认翻译方向无法找到合适词典的时候，使用该设置。通常设置成自己的母语。
- 设置方法
  - 以`default-in`设置成`en`为例子:`sd --config DEFAULT_LAN DEFAULT_LANG_IN en`
  - 以`default-out`设置成`zh`为例子:`sd --config DEFAULT_LAN DEFAULT_LANG_OUT zh`




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
细节参考`sd -h`。在NAT后面的时候，这个还是很重要的（比如公司里）。当然不能每次都这样输入，你可能需要自己把脚本再包装一下了。或者考虑增加配置文件，有需求再说吧。
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
也可以添加多条，如：
`-p http=socks5h://127.0.0.1:1080@https=socks5h://127.0.0.1:1080`。proxy的格式请参考Python包`requests`中关于`Proxies`的设置。


# 词典库
目标是添加各种各样的翻译方向。我自己的工作环境只用到中日英，现在只有几种先用着，以后慢慢添加。有需要的留言。`sd -l`打印所有可用的词典。
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


## 自己添加词典库
可以在issue留言（希望可以提供一个可靠的在线源），等不及了可以在源代码里面添加。需要会对`BeautifulSoup`懂一点。以下是"有道 中英"词典的例子。类的名字一定要用`DICTIONARY_`打头，用来扫描的。
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



# 恢复默认设置
`sd --reset`
