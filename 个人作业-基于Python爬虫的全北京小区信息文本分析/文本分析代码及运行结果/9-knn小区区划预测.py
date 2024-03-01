import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import numpy as np

def plot_confusion_matrix(y, yp, filename):
    """可视化混淆矩阵并保存为 JPG 文件"""
    cm = confusion_matrix(y, yp)
    plt.figure(figsize=(10, 10))  # 设置图形的尺寸
    plt.matshow(cm, cmap=plt.cm.Blues, fignum=1)  # fignum 参数指定要操作的图形编号
    plt.colorbar()
    for x in range(len(cm)):
        for y in range(len(cm)):
            plt.annotate(cm[x, y], xy=(y, x), horizontalalignment='center', verticalalignment='center')
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig(filename)  # 保存为 JPG 文件
    plt.show()

import re

def extract_number(text):
    """提取数字"""
    digits = re.findall(r'\d+\.*\d*', str(text))
    if digits:
        return float(digits[0])
    return pd.NA

def process_data(data):
    """数据预处理"""
    # 选择需要的列
    data = data[['建造年份', '房价', '在售房数', '建筑材质','区划','区域']].copy()

    # 对'建造年份'列进行处理，提取年份作为数值特征
    data.loc[:, '建造年份'] = data['建造年份'].str.extract('(\d{4})').astype(float)

    # 对'房价'列进行处理，提取数字部分并转换为数值特征
    data.loc[:, '房价'] = data['房价'].apply(extract_number)

    # 处理'在售房数'列，提取数字部分并转换为数值特征
    data.loc[:, '在售房数'] = data['在售房数'].apply(extract_number)

    # 将非数值特征编码为数值
    label_encoder = LabelEncoder()
    data.loc[:, '建筑材质'] = label_encoder.fit_transform(data['建筑材质'])
    data.loc[:, '区划'] = label_encoder.fit_transform(data['区划'])
    data.loc[:, '区域'] = label_encoder.fit_transform(data['区域'])

    # 用每列的中位数填充缺失值
    data.fillna(data.median(), inplace=True)

    return data




def main():
    """主函数"""
    data = pd.read_excel(r'1-北京小区数据.xlsx')

    # 数据预处理
    processed_data = process_data(data)

    # 将数据集拆分为特征集和目标变量
    X_whole = processed_data.drop('区划', axis=1)
    y_whole = processed_data['区划']

    # 将数据集拆分为训练集和测试集
    x_train_w, x_test_w, y_train_w, y_test_w = train_test_split(X_whole, y_whole, test_size=0.2, random_state=0)

    # 使用K近邻分类器进行模型训练
    knn = KNeighborsClassifier(n_neighbors=10)
    knn.fit(x_train_w, y_train_w)

    # 预测训练集并输出分类报告和混淆矩阵
    train_predicted = knn.predict(x_train_w)
    train_report = classification_report(y_train_w, train_predicted, output_dict=True)
    train_cm = confusion_matrix(y_train_w, train_predicted)
    print("Train Classification Report:")
    print(train_report)

    # 保存训练集的分类报告和混淆矩阵
    pd.DataFrame(train_report).transpose().to_csv('9-knn训练集分类报告.csv')
    plot_confusion_matrix(y_train_w, train_predicted, '9-knn训练集混淆矩阵.jpg')

    # 预测测试集并输出分类报告和混淆矩阵
    test_predicted = knn.predict(x_test_w)
    test_report = classification_report(y_test_w, test_predicted, output_dict=True)
    test_cm = confusion_matrix(y_test_w, test_predicted)
    print("Test Classification Report:")
    print(test_report)


    # 保存测试集的分类报告和混淆矩阵
    pd.DataFrame(test_report).transpose().to_csv('9-knn测试集分类报告.csv')
    plot_confusion_matrix(y_test_w, test_predicted, '9-knn测试集混淆矩阵.jpg')


if __name__ == "__main__":
    main()