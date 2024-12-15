import json

# 打开并读取 JSON 文件
with open('file.json', 'r', encoding='utf-8') as file:
    data = json.load(file)  # 使用 json.load() 解析 JSON 文件
    data = data['data']
    for item in data:
        print(item)
