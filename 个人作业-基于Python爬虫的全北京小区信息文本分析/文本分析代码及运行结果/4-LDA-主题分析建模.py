import pandas as pd  # 导入 pandas 模块
from gensim import corpora  # 用于构建文本的字典和语料库
import jieba  # 中文分词工具
import pyLDAvis.gensim  # 用于LDA主题模型可视化
import matplotlib.pyplot as plt  # 用于绘图
import matplotlib  # matplotlib 库
from gensim.models.coherencemodel import CoherenceModel  # 用于计算主题一致性
from gensim.models.ldamodel import LdaModel  # LDA主题模型
import warnings  # 用于警告处理
import jieba.posseg as pseg  # 结巴分词词性标注工具

warnings.filterwarnings('ignore')  # 忽略警告
jieba.setLogLevel(jieba.logging.INFO)  # 设置结巴分词的日志级别


# 计算困惑度
def perplexity(ldamodel, corpus):
    return ldamodel.log_perplexity(corpus)


"""
    计算LDA模型的困惑度

    参数:
    ldamodel: gensim中的LDA模型对象
    corpus: 文档语料库的词袋表示形式

    返回值:
    float: LDA模型的困惑度
    """


# 计算 coherence 主题一致性
def coherence(ldamodel, texts, dictionary, corpus):
    coh = []
    for num_topics in range(1, 11):
        ldamodel = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=30, random_state=1)
        print(ldamodel.print_topics(num_topics=num_topics, num_words=10))
        ldacm = CoherenceModel(model=ldamodel, texts=texts, dictionary=dictionary, coherence='c_v', corpus=corpus)
        coh.append(ldacm.get_coherence())
    return coh


"""
    计算LDA模型的coherence主题一致性得分

    参数:
    ldamodel: gensim中的LDA模型对象
    texts: 文档列表，每个文档包含单词的列表
    dictionary: gensim中的词典对象
    corpus: 文档语料库的词袋表示形式

    返回值:
    list: 包含不同主题数目下的coherence得分的列表
    """


# 修改数据清理和分词函数
def tokenize_file(file_path):
    """对文件进行分词，并选择名词进行保留"""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
        words = pseg.cut(data)  # 使用 jieba 的词性标注功能
        stopword = {line.strip() for line in open("StopwordsCN.txt", encoding='utf-8')}
        filtered_words = [word for word, flag in words if
                          (flag.startswith('n') or flag.startswith('a')) and word.strip() and word not in stopword]
        return filtered_words


"""
    对文件进行分词，并选择名词进行保留

    参数:
    file_path: 文件路径字符串

    返回值:
    list: 分词后的词汇列表
    """
if __name__ == '__main__':
    file_paths = ['3-小区命名.txt', '3-小区介绍.txt', '3-周边配套.txt']

    for idx, file_path in enumerate(file_paths, start=1):
        print(f"Processing file {idx}: {file_path}")
        df_data = tokenize_file(file_path)

        train = [[word] for word in df_data]

        dictionary = corpora.Dictionary(train)
        corpus = [dictionary.doc2bow(text) for text in train]

        print("词典构建完成")

        ldamodel = LdaModel(corpus=corpus, id2word=dictionary, num_topics=5, passes=80, random_state=0)
        """
         LdaModel 参数说明：
         corpus: 语料库，文档-词袋格式。
         num_topics: 主题数量。
         id2word: 词袋模型对应的词典。
         passes: 迭代次数。
         random_state: 随机数种子。
         """
        topic_list = ldamodel.print_topics()
        print(topic_list)
        # 获取每个主题中的所有词汇和权重
        topics_words = ldamodel.show_topics(formatted=False, num_words=10000)  # 每个主题显示所有词汇

        # 创建一个空的 DataFrame 以保存主题词汇和权重
        topics_data = pd.DataFrame(columns=['主题', '词汇', '权重'])

        # 将词汇和权重添加到 DataFrame
        for idx, topic in topics_words:
            words = [word for word, _ in topic]
            weights = [weight for _, weight in topic]
            topic_df = pd.DataFrame({'主题': [idx + 1] * len(words), '词汇': words, '权重': weights})
            topics_data = pd.concat([topics_data, topic_df], ignore_index=True)

        # 将结果保存到 CSV 文件
        csv_file = f'4-{file_path.split("-")[-1].replace(".txt", "")}-LDA主题.csv'
        topics_data.to_csv(csv_file, index=False)
        print(f"Saved topics words and weights to CSV file: {csv_file}")

        data = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary)
        html_file = f'4-{file_path.split("-")[-1].replace(".txt", "")}-LDA主题分析建模.html'
        pyLDAvis.save_html(data, html_file)
        print(f"Saved HTML visualization: {html_file}")

        x = range(1, 11)

        z = [perplexity(ldamodel, corpus) for i in x]
        print(z)
        plt.plot(x, z)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.xlabel('主题数目')
        plt.ylabel("困惑度")
        matplotlib.rcParams['axes.unicode_minus'] = False
        plt.title('主题-困惑度变化情况统计')
        plt.savefig(f'4-{file_path.split("-")[-1].replace(".txt", "")}-LDA-perplexity.png')  # 先保存再显示
        plt.show()
        print(f"Perplexity plot {idx} completed")

        # 计算 coherence 并生成图表
        y = coherence(ldamodel, train, dictionary, corpus)
        print(y)
        plt.plot(x, y)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.xlabel('主题数目')
        plt.ylabel("coherence大小")
        matplotlib.rcParams['axes.unicode_minus'] = False
        plt.title('主题-coherence变化情况统计')
        plt.savefig(f'4-{file_path.split("-")[-1].replace(".txt", "")}-LDA-coherence.png')  # 先保存再显示
        plt.show()
        print(f"Coherence plot {idx} completed")
