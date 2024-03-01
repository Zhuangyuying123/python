import pandas as pd  # 导入Pandas库用于数据处理

# 读取Excel文件
excel_file1 = pd.ExcelFile('2-北京小区简介数据.xlsx')  # 读取包含小区简介数据的Excel文件
excel_file2 = pd.ExcelFile('1-北京小区数据.xlsx')  # 读取包含北京小区数据的Excel文件

# 读取第三列和第四列数据
df1 = excel_file1.parse(excel_file1.sheet_names[0])  # 解析第一个Excel文件的第一个表单数据
column_3_data = df1.iloc[:, 2]  # 获取第一个Excel文件中的第三列数据
column_4_data = df1.iloc[:, 3]  # 获取第一个Excel文件中的第四列数据
df2 = excel_file2.parse(excel_file2.sheet_names[0])  # 解析第二个Excel文件的第一个表单数据
column_5_data = df2.iloc[:, 0]  # 获取第二个Excel文件中的第一列数据

# 将第三列数据保存为小区介绍.txt
with open('3-小区介绍.txt', 'w', encoding='utf-8') as file:
    for item in column_3_data:
        file.write("%s\n" % item)  # 将第三列数据逐行写入小区介绍文件

# 将第四列数据保存为周边配套.txt
with open('3-周边配套.txt', 'w', encoding='utf-8') as file:
    for item in column_4_data:
        file.write("%s\n" % item)  # 将第四列数据逐行写入周边配套文件

# 将第一列数据保存为小区命名.txt
with open('3-小区命名.txt', 'w', encoding='utf-8') as file:
    for item in column_5_data:
        file.write("%s\n" % item)  # 将第一列数据逐行写入小区命名文件

# 处理停用词
stopwords = set()  # 创建空集合用于存储停用词
with open('StopwordsCN.txt', 'r', encoding='utf-8') as file:
    for line in file:
        stopwords.add(line.strip())  # 读取并存储停用词

# 处理小区介绍.txt
with open('3-小区介绍.txt', 'r', encoding='utf-8') as file:
    text = file.read()  # 读取小区介绍文件内容
    text = ' '.join(word for word in text.split() if word not in stopwords)  # 移除停用词并重新组合文本内容

with open('3-小区介绍.txt', 'w', encoding='utf-8') as file:
    file.write(text)  # 将处理后的文本内容写入小区介绍文件

# 处理周边配套.txt
with open('3-周边配套.txt', 'r', encoding='utf-8') as file:
    text = file.read()  # 读取周边配套文件内容
    text = ' '.join(word for word in text.split() if word not in stopwords)  # 移除停用词并重新组合文本内容

with open('3-周边配套.txt', 'w', encoding='utf-8') as file:
    file.write(text)  # 将处理后的文本内容写入周边配套文件

# 处理小区命名.txt
with open('3-小区命名.txt', 'r', encoding='utf-8') as file:
    text = file.read()  # 读取小区命名文件内容
    text = ' '.join(word for word in text.split() if word not in stopwords)  # 移除停用词并重新组合文本内容

with open('3-小区命名.txt', 'w', encoding='utf-8') as file:
    file.write(text)  # 将处理后的文本内容写入小区命名文件