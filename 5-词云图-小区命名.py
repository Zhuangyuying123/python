# 导入必要的库
import matplotlib.pyplot as plt  # 用于绘制图表
from wordcloud import WordCloud  # 用于生成词云图
import jieba  # 用于中文分词
import imageio.v2 as imageio  # 导入图像处理库
import re  # 用于正则表达式操作
from PIL import Image  # 导入PIL库，用于图像处理

# 打开并读取txt文件内容
file = open("3-小区命名.txt", encoding='utf-8')
article = file.read()
file.close()

# 使用jieba进行中文分词
seg_str = jieba.cut(article, cut_all=False)
liststr = "/".join(seg_str)

# 删除文本中的所有数字
article_no_numbers = re.sub(r'\d+', '', liststr)

# 打开并读取停用词文件
stopwords_path = "StopwordsCN.txt"
f_stop = open(stopwords_path, encoding='utf-8')
f_stop_text = f_stop.read()
f_stop.close()

# 创建停用词列表
mywordlist = []

# 将停用词读取并放入列表中
f_stop_seg_list = f_stop_text.split("\n")
for myword in article_no_numbers.split('/'):
    # 剔除停用词和长度小于等于1的词
    if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
        mywordlist.append(myword)

# 创建空字典存储词频统计
word_freq = {}

# 对每个词进行词频统计
for myword in mywordlist:
    word_freq[myword] = word_freq.get(myword, 0) + 1

# 按词频降序排列
sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

# 提取词频前140的词和词频140-270的词
top_140_words = dict(sorted_word_freq[:140])
words_140_to_270 = dict(sorted_word_freq[140:270])

# 载入背景图片
bg_mask = "5-词云图素材-房子简笔画.jpg"  # 背景图片路径
mask_img = imageio.imread(bg_mask)  # 使用PIL库打开图像文件

# 生成词云图1（词频前140的词）
wordcloud1 = WordCloud(font_path='msyh.ttc', background_color='white', mask=mask_img).generate_from_frequencies(top_140_words)
wordcloud1.to_file("5-词云图-小区命名1.jpg")

# 生成词云图2（词频140-270的词）
wordcloud2 = WordCloud(font_path='msyh.ttc', background_color='white', mask=mask_img, max_font_size=60).generate_from_frequencies(words_140_to_270)
wordcloud2.to_file("5-词云图-小区命名2.jpg")

# 绘制词云图1
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud1, interpolation='bilinear')
plt.axis("off")
plt.show()

# 绘制词云图2
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud2, interpolation='bilinear')
plt.axis("off")
plt.show()
