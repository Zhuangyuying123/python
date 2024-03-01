# 导入必要的库
import re  # 用于正则表达式的处理
import os  # 用于文件路径操作
import jieba.analyse  # 结巴分词中的关键词提取工具
import matplotlib.pyplot as plt  # 用于绘图
import pandas as pd  # 用于数据处理
import numpy as np  # 用于数值计算
from sklearn.feature_extraction.text import TfidfVectorizer  # 用于构建 TF-IDF 特征矩阵
from sklearn.decomposition import PCA  # 用于主成分分析（PCA）

# 停用词文件路径
stopwords_path = "StopwordsCN.txt"

# 设置结巴分词的停用词表
jieba.analyse.set_stop_words(stopwords_path)

# 要处理的文件名列表
file_names = ['3-周边配套.txt', '3-小区介绍.txt', '3-小区命名.txt']

# 遍历每个文件
for file_name in file_names:
    # 读取文件内容
    data_path = os.path.join(os.getcwd(), file_name)
    text = open(data_path, "r", encoding="utf-8").read()

    # 使用jieba进行关键词提取（TF-IDF方法）
    result0 = jieba.analyse.extract_tags(text, topK=400, withWeight=True)
    print(result0)

    # 构建关键词与词频占比的数据框
    result_dict = dict(result0)
    test = pd.DataFrame(result_dict.items(), columns=["关键词", "词频占比"])

    # 生成输出的CSV文件名
    chinese_part = re.findall(r'[\u4e00-\u9fa5]+', file_name)
    csv_name = "7-" + chinese_part[0] + "-TF-IDF关键词提取.csv"

    # 将结果保存到CSV文件
    test.to_csv(csv_name, encoding="gbk")

    # 从CSV文件读取数据
    data = pd.read_csv(csv_name, encoding="gbk")

    # 构建 TF-IDF 特征矩阵
    corpus = data['关键词'].values.tolist()
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)

    # 使用PCA进行二维降维
    pca = PCA(n_components=2)  # 降至二维
    X_pca = pca.fit_transform(X.toarray())

    # 可视化降维后的数据
    plt.figure(figsize=(10, 5))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.5)
    plt.title(f'PCA Visualization of TF-IDF - {file_name}')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    image_name = "7-" + chinese_part[0] + "-TF-IDF关键词提取.jpg"
    plt.savefig(image_name)  # 保存图像为文件
    plt.show()  # 显示图像
