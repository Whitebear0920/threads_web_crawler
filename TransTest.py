import jieba
import jieba.analyse
import nltk
import re
import asyncio
from googletrans import Translator

async def smart_translate(text, target='zh-tw'):
    # 拆成中英文段落
    segments = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z0-9,\'\s?]+', text)
    translated_segments = []

    async with Translator() as translator:
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue
            # 若包含英文字母才翻譯
            if re.search('[a-zA-Z]', seg):
                result = await translator.translate(seg, src='en', dest=target)
                translated_segments.append(result.text)
            else:
                translated_segments.append(seg)

    return ''.join(translated_segments)

# 測試用句子
post = "我今天心情不錯，I'm fine thank you and you?"

# 非同步執行翻譯
print(asyncio.run(smart_translate(post)))

"""print(list(jieba.cut(post)))
tokenizer = nltk.RegexpTokenizer(r'\w+|\'\w+', gaps = False)
post = tokenizer.tokenize(post)
print(post)
new_post = list()
for i in post:
    if i[0]>"z":
        #print(list(jieba.cut(i)))
        for j in list(jieba.cut(i)):
            new_post.append(j)
    else:
        new_post.append(i)
print(new_post)
"""