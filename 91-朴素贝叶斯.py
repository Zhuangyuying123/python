import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import re

def cm_plot(y, yp, filename):
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
    data = pd.read_excel('1-北京小区数据.xlsx')

    # 数据预处理
    processed_data = process_data(data)

    X_whole = processed_data.drop('区划', axis=1)
    y_whole = processed_data['区划']

    # 将数据集拆分为训练集和测试集
    x_train_w, x_test_w, y_train_w, y_test_w = train_test_split(X_whole, y_whole, test_size=0.2, random_state=0)

    # 使用朴素贝叶斯分类器进行模型训练
    classifier = MultinomialNB(alpha=1)
    classifier.fit(x_train_w, y_train_w)

    # 预测训练集并输出分类报告和混淆矩阵
    train_predicted = classifier.predict(x_train_w)
    train_report = classification_report(y_train_w, train_predicted, output_dict=True)
    print("Train Classification Report:")
    print(train_report)
    cm_plot(y_train_w, train_predicted, '91-朴素贝叶斯-训练集混淆矩阵.jpg')  # 保存混淆矩阵为 JPG 文件

    # 保存训练集的分类报告
    pd.DataFrame(train_report).transpose().to_csv('91-朴素贝叶斯-训练集分类报告.csv')

    # 预测测试集并输出分类报告和混淆矩阵
    test_predicted = classifier.predict(x_test_w)
    test_report = classification_report(y_test_w, test_predicted, output_dict=True)
    print("Test Classification Report:")
    print(test_report)
    cm_plot(y_test_w, test_predicted, '91-朴素贝叶斯-测试集混淆矩阵.jpg')  # 保存混淆矩阵为 JPG 文件

    # 保存测试集的分类报告
    pd.DataFrame(test_report).transpose().to_csv('91-朴素贝叶斯-测试集分类报告.csv')

if __name__ == "__main__":
    main()