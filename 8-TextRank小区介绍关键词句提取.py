# 导入所需模块
import imageio.v2 as imageio
from matplotlib import pyplot as plt
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from wordcloud import WordCloud
import jieba.analyse


# 从文件中读取文本内容
def read_text_from_file(file_path):
    """
    读取指定文件的文本内容。

    Parameters:
    - file_path (str): 文件路径。

    Returns:
    - str: 读取到的文本内容。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# 提取关键词
def keywords_extraction(text):
    """
    使用 TextRank4Keyword 进行关键词分析。

    Parameters:
    - text (str): 待分析的文本。

    Returns:
    - list: 包含关键词的列表。
    """
    tr4w = TextRank4Keyword()
    tr4w.analyze(text, window=2, lower=True)
    keywords = tr4w.get_keywords(num=100, word_min_len=2)
    return [item.word for item in keywords]


# 生成词云
def generate_wordcloud(keywords, title, bg_image):
    """
    生成并展示词云图。

    Parameters:
    - keywords (list): 包含关键词的列表。
    - title (str): 词云图的标题。
    - bg_image (str): 背景图片的路径。

    Returns:
    - None
    """
    keywords_str = ' '.join(keywords)
    imgbg = imageio.imread(bg_image)
    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path='msyh.ttc', mask=imgbg).generate(
        keywords_str)
    plt.figure(figsize=(10, 5))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Word Cloud - {title}')
    wordcloud.to_file(f"{title}.png")
    plt.show()


# 提取关键短语
def keyphrases_extraction(text):
    """
    使用 TextRank4Keyword 进行关键短语分析。

    Parameters:
    - text (str): 待分析的文本。

    Returns:
    - list: 包含关键短语的列表。
    """
    tr4w = TextRank4Keyword()
    tr4w.analyze(text, window=2, lower=True)
    keyphrases = tr4w.get_keyphrases(keywords_num=20, min_occur_num=1)
    return keyphrases


# 提取关键句子
def keysentences_extraction(text):
    """
    使用 TextRank4Sentence 进行关键句子分析。

    Parameters:
    - text (str): 待分析的文本。

    Returns:
    - list: 包含关键句子的列表。
    """
    tr4s = TextRank4Sentence()
    tr4s.analyze(text, lower=True)
    keysentences = tr4s.get_key_sentences(num=5)
    return keysentences


if __name__ == "__main__":
    # 文件路径
    data_path = r'3-小区介绍.txt'
    bg_image_path = "5-词云图素材-房子简笔画.jpg"

    # 从文件中读取文本内容
    text = read_text_from_file(data_path)

    # 提取关键词并生成词云图
    keywords = keywords_extraction(text)
    generate_wordcloud(keywords, '小区介绍关键词词云', bg_image_path)

    # 提取关键短语并打印输出
    keyphrases = keyphrases_extraction(text)
    print(keyphrases)

    # 提取关键句子并打印输出
    keysentences = keysentences_extraction(text)
    print(keysentences)
