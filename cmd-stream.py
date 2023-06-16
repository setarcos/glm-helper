import requests
import readline
import traceback
import os

# 指定 API 接口的基础 URL 和 headers
api_url = "http://127.0.0.1:8000"
headers = {"Content-Type": "application/json"}

# 打印欢迎语句和提示信息
print("Welcome to the chatbot! Type 'exit' to quit.")
print("=" * 50)
payload = {"prompt": "",
           "temperature": 0.2,
           "history":[]}
payload['history'] = [["你好","你好！我是人工智能助手 ChatGLM-6B，很高兴见到你，欢迎问我任何问题。"]]
while True:
    # 读取用户输入的对话内容
    user_input = input("You: ")
    payload['prompt'] = user_input

    # 如果用户输入 'exit'，则退出聊天程序
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    
    # 如果用户输入 'history'，则输出聊天历史记录
    if user_input.lower() == 'history':
        for i, (user_text, bot_text) in enumerate(payload['history']):
            print(f"[{i+1}] You: {user_text}")
            print(f"     Bot: {bot_text}")
        continue  # 继续下一轮循环

    # 清空历史
    if user_input.lower() == 'clear':
        payload['history'] = []
        continue

    if user_input == '':
        continue

    # 构造请求体并发送 POST 请求
    response = requests.post(api_url, json=payload, headers=headers, stream=True)
    # response.encoding = 'utf-8'
    # 检查响应状态码
    last_line = ''
    try:
        if response.status_code == 200:
            # 逐行迭代接收数据
            for line in response.iter_content(chunk_size=None):
                if line:
                    # 找到回答的起始标记
                    idx = line.rfind(b'<^>')
                    if (idx < 0):
                        continue
                    # 解码为 UTF-8 字符串
                    utf8_line = line[idx+3:].decode('utf-8')
                    # 在这里处理每行接收到的数据
                    last_line = utf8_line
                    os.system('clear')
                    print(last_line, flush=True)
        else:
            print("请求失败:", response.status_code)
    except:
        err = traceback.format_exc()
        print(err)
    # 将本轮对话加入历史记录
    payload['history'].append([user_input, last_line])
    # print(payload)

