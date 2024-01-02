


class OnlineAPI():
    
    def __init__(self,req):
        self.req = req 
    
    
    def getHeaders(self):
        headers = {
            'authority': 'transmart.qq.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,zh-CN;q=0.6',
            'content-type': 'application/json',
            'origin': 'https://transmart.qq.com',
            'referer': 'https://transmart.qq.com/zh-CN/index',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        }
        return headers
    
    def getTranseText(self,lanIn,lanOut,context):
        json_data = {
            'header': {
                'fn': 'auto_translation',
            },
            'type': 'plain',
            'model_category': 'normal',
            'source': {
                'lang': lanIn,
                'text_list': [
                    '',
                    context,
                    '',
                ],
            },
            'target': {
                'lang': lanOut,
            },
        }
        url = 'https://transmart.qq.com/api/imt'
        d = self.req.postJson(url, headers=self.getHeaders(), json=json_data)
        if 'auto_translation' in d: 
            return d['auto_translation'][1]
        else:
            return None
        
     # 
#     def detectLanguage(self,context):
#         headers = self.getHeaders()
#         json_data = {
#             'header': {
#                 'fn': 'text_analysis',
# #                 'client_key': 'browser-chrome-110.0.0-Windows 10-f58c2490-c39e-4ec3-88ad-0d8c83a8a43c-1678416362238',
#             },
#             'text': context,
#             'type': 'plain',
#             'normalize': {
#                 'merge_broken_line': False,
#             },
#         }
#         response = requests.post('https://transmart.qq.com/api/imt', headers=headers, json=json_data)
#         return response.json()['language']
    

    def translate(self,inputText):
        cookies = {
    #         'client_key': 'browser-chrome-110.0.0-Windows%2010-f58c2490-c39e-4ec3-88ad-0d8c83a8a43c-1678416362238',
        }

        headers = self.getHeaders()
        
        lang = self.detectLanguage(inputText)
        
        if lang == "zh":
            targetLang = 'en'
        else:
            targetLang = 'zh'

        json_data = {
            'header': {
                'fn': 'auto_translation',
    #             'client_key': 'browser-chrome-110.0.0-Windows 10-f58c2490-c39e-4ec3-88ad-0d8c83a8a43c-1678416362238',
            },
            'type': 'plain',
            'model_category': 'normal',
            'source': {
                'lang': lang,
                'text_list': [
                    '',
                    inputText,
                    '',
                ],
            },
            'target': {
                'lang': targetLang,
            },
        }
        response = requests.post('https://transmart.qq.com/api/imt', cookies=cookies, headers=headers, json=json_data)
        resJson = response.json()
        if 'auto_translation' in resJson: 
            return resJson['auto_translation'][1]
        else:
            return "[不用翻译？]"

