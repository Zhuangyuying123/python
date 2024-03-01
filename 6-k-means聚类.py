# 导入必要的库
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import re
import matplotlib.pyplot as plt

# 读取Excel文件中的数据
df = pd.read_excel('1-北京小区数据.xlsx', sheet_name='Sheet1')


# 数据预处理

# 处理销售情况数据：提取成交数量和正在出租的数量
def extract_sales(text):
    """
    从销售情况文本中提取成交数量和正在出租的数量。

    参数:
    - text: 销售情况文本

    返回:
    - 成交数量, 正在出租数量
    """
    # 通过正则表达式提取所有数字
    digits = re.findall(r'\d+', str(text))

    if digits:
        # 返回第一个数字作为成交数量，最后一个数字作为正在出租数量
        return int(digits[0]), int(digits[-1])
    return pd.NA, pd.NA


# 应用extract_sales函数到 '销售情况' 列，并将结果分别赋给 '成交数量' 和 '正在出租' 列
df['成交数量'], df['正在出租'] = zip(*df['销售情况'].apply(extract_sales))


# 处理房价数据：提取数字并转换为浮点数
def extract_price(text):
    """
    从房价文本中提取数字并转换为浮点数。

    参数:
    - text: 房价文本

    返回:
    - 房价（浮点数）
    """
    if '万' in str(text):
        # 通过正则表达式提取所有数字（包括小数）
        digits = re.findall(r'\d+\.*\d*', str(text))

        if digits:
            # 返回提取的数字作为浮点数
            return float(digits[0])
    return pd.NA


# 应用extract_price函数到 '房价' 和 '在售房数' 列
df['房价'] = df['房价'].apply(extract_price)
df['在售房数'] = df['在售房数'].apply(extract_price)

# 特征提取
selected_features = ['建筑材质', '房价', '在售房数', '成交数量', '正在出租']

# 将分类变量转换为数值型数据
label_encoder = LabelEncoder()
# 使用LabelEncoder将 '建筑材质' 列中的文本标签转换为数字
df['建筑材质'] = label_encoder.fit_transform(df['建筑材质'])

# 创建特征矩阵X
X = df[selected_features]

# 将缺失值用0填充
X.fillna(0, inplace=True)

# 实例化KMeans模型并应用于数据
kmeans = KMeans(n_clusters=7)  # 设置聚类的数量
clusters = kmeans.fit_predict(X)

# 将聚类结果添加到原始数据中
df['Cluster'] = clusters

# 打印聚类结果
print(df[['小区名称', 'Cluster']])
# 将结果保存为CSV文件
df.to_csv('6-kmeans结果.csv', index=False)

# 可视化聚类结果
plt.figure(figsize=(8, 6))
for i in range(7):
    # 根据每个聚类结果绘制散点图
    plt.scatter(X[clusters == i]['房价'], X[clusters == i]['正在出租'], label=f'Cluster {i}')

# 绘制聚类中心点
plt.scatter(kmeans.cluster_centers_[:, 1], kmeans.cluster_centers_[:, 4], s=100, c='black', label='Centroids')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.xlabel('房价', loc='right')
plt.ylabel('在售房数', loc='top')
plt.title('K-means Clustering Visualization')
plt.legend()
# 将图表保存为图片文件
plt.savefig("6-k-means聚类.jpg")
plt.show()
