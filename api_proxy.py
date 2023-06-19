import time
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from UltraDict import UltraDict
import json, uuid
import requests
import time

status = UltraDict(name='fastapi_dict')

server_list = []

# 初始化服务器列表
def init_dict():
    with open('servers.txt', 'r') as f:
        for line in f:
            line = line.strip()
            server_list.append(line)

init_dict()
with status.lock:
    if not status.has_key('init'):
        status['init'] = True # 保证初始化一次
        status['ready'] = len(server_list)
        for i, server in enumerate(server_list):
            status[str(i)] = False

app = FastAPI()
headers = {"Content-Type": "application/json"}
payload = {"prompt": "",
           "temperature": 0.2,
           "history":[]}
# 生成数据的生成器函数
async def generate_data(index):
    url = 'http://' + server_list[index]
    response = requests.post(url, json=payload, headers=headers, stream=True)
    for line in response.iter_content(chunk_size=None):
        idx = line.rfind(b'<^>')
        message = json.dumps(dict(
            role = "AI",
            id = "chatglm",
            parentMessageId = None,
            text = line[idx+3:].decode('utf-8'),
        ))
        yield "<^>" + message
    with status.lock:
        status[str(index)] = False
        status['ready'] += 1

@app.get("/status")
async def get_status():
    return {"ready", status['ready']}

@app.post("/")
async def stream_data(data: dict):
    idx = 0
    while True:
        if idx == len(server_list):
            idx = 0
            time.sleep(0.1)
        with status.lock:
            if not status[str(idx)]:
                status[str(idx)] = True
                status['ready'] -= 1
                break;
        idx += 1
    print(f"Using {idx}\n")
    return StreamingResponse(generate_data(idx), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_proxy:app", host="127.0.0.1", port=3002, workers=4)
