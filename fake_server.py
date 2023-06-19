import time
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse, JSONResponse

app = FastAPI()
# 生成数据的生成器函数
async def generate_data():
    for i in range(10):
        # 每个数据点之间等待 1 秒钟
        time.sleep(1)
        data = f"<^>Data point {i}\n"
        yield data

@app.post("/")
async def stream_data(data: dict):
    print(data)
    return StreamingResponse(generate_data())

@app.post("/config")
async def config():
    return JSONResponse(content=dict(
        message=None,
        status="Success",
        data=[]
    ))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fake_server:app", host='0.0.0.0', port=3002, workers=1)
