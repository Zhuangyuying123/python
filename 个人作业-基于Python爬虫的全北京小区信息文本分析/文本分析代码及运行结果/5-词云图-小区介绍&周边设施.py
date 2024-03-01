# 导入必要的库
import matplotlib.pyplot as plt  # 用于绘制图表
from wordcloud import WordCloud  # 生成词云图的库
import jieba  # 中文分词库
import imageio  # 用于读取图像文件的库
import re  # 正则表达式库，用于文本处理
from PIL import Image  # PIL库用于处理图像

# 读取两个txt文件中的内容
file1 = open("3-小区介绍.txt", encoding='utf-8')
file2 = open("3-周边配套.txt", encoding='utf-8')
article1 = file1.read()
article2 = file2.read()
file1.close()
file2.close()

# 使用jieba进行分词处理
seg_str1 = jieba.cut(article1, cut_all=False)
seg_str2 = jieba.cut(article2, cut_all=False)

liststr1 = "/".join(seg_str1)  # 连接分词结果
liststr2 = "/".join(seg_str2)

# 删除文本中的所有数字
article_no_numbers1 = re.sub(r'\d+', '', liststr1)
article_no_numbers2 = re.sub(r'\d+', '', liststr2)

# 打开停用词文件
stopwords_path = "StopwordsCN.txt"
f_stop = open(stopwords_path, encoding='utf-8')
f_stop_text = f_stop.read()
f_stop.close()

# 创建空列表存储最终的词
mywordlist1 = []
mywordlist2 = []
f_stop_seg_list = f_stop_text.split("\n")

# 过滤停用词，将不在停用词表中且长度大于1的词存入列表
for myword1 in article_no_numbers1.split('/'):
    if not (myword1.strip() in f_stop_seg_list) and len(myword1.strip()) > 1:
        mywordlist1.append(myword1)

for myword2 in article_no_numbers2.split('/'):
    if not (myword2.strip() in f_stop_seg_list) and len(myword2.strip()) > 1:
        mywordlist2.append(myword2)

# 创建字典存储词频统计
word_freq1 = {}
word_freq2 = {}

# 统计每个词的词频
for myword in mywordlist1:
    word_freq1[myword] = word_freq1.get(myword, 0) + 1

for myword in mywordlist2:
    word_freq2[myword] = word_freq2.get(myword, 0) + 1

# 按词频降序排列
sorted_word_freq1 = sorted(word_freq1.items(), key=lambda x: x[1], reverse=True)
sorted_word_freq2 = sorted(word_freq2.items(), key=lambda x: x[1], reverse=True)

# 提取词频前140的词
top_140_words1 = dict(sorted_word_freq1[:140])
top_140_words2 = dict(sorted_word_freq2[:140])

# 输出词频前140的词
print(top_140_words1)
print(top_140_words2)

# 载入背景图片
bg_mask = "5-词云图素材-房子简笔画2.jpg"  # 背景图片路径
mask_img = imageio.imread(bg_mask)  # 使用imageio库打开图像文件

# 生成词云图1（词频前140的词）
wordcloud1 = WordCloud(font_path='msyh.ttc', background_color='white', mask=mask_img).generate_from_frequencies(top_140_words1)
wordcloud1.to_file("5-词云图-小区介绍.jpg")

# 生成词云图2（词频前140的词）
wordcloud2 = WordCloud(font_path='msyh.ttc', background_color='white', mask=mask_img).generate_from_frequencies(top_140_words2)
wordcloud2.to_file("5-词云图-周边设施.jpg")

# 绘制词云图1
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud1, interpolation='bilinear')  # 使用双线性插值的方式渲染图像
plt.axis("off")  # 不显示坐标轴
plt.show()

# 绘制词云图2
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud2, interpolation='bilinear')  # 使用双线性插值的方式渲染图像
plt.axis("off")  # 不显示坐标轴
plt.show()
