import requests
import readline

# 指定 API 接口的基础 URL 和 headers
api_url = "http://127.0.0.1:8000"
headers = {"Content-Type": "application/json"}

# 打印欢迎语句和提示信息
print("Welcome to the chatbot! Type 'exit' to quit.")
print("=" * 50)
payload = {"prompt": "",
           "history":[]}

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
    response = requests.post(api_url, json=payload, headers=headers).json()

    # 输出 ChatGLM 返回的回复文本
    bot_text = response['response']
    payload['history'] = response['history']
    print("Bot:", bot_text)

