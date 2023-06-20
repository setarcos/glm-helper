from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from transformers import AutoTokenizer, AutoModel
import uvicorn, json, datetime
import torch
import asyncio
from utils import load_model_on_gpus

app = FastAPI()

max_length=2048
top_p = 0.7
temperature = 0.9

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
# model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()
model = load_model_on_gpus("THUDM/chatglm-6b", num_gpus=2)
model.eval()

async def process(prompt, history):
    try:
        for response, history in model.stream_chat(tokenizer, prompt, history,
                                   max_length=max_length if max_length else 2048,
                                   top_p=top_p if top_p else 0.7,
                                   temperature=temperature if temperature else 0.95):
            await asyncio.sleep(0) # 这里必须加上这句才能捕获用户中断
            yield "<^>" + response
    except asyncio.CancelledError:
        # Force stop
        pass

@app.post("/")
async def create_item(request: Request):
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    prompt = json_post_list.get('prompt')
    history = json_post_list.get('history')
    max_length = json_post_list.get('max_length')
    top_p = json_post_list.get('top_p')
    temperature = json_post_list.get('temperature')
    return StreamingResponse(process(prompt, history))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, workers=1)
