# ChatGLM 的辅助脚本

## 脚本简介

在部署[ChatGLM-6B 模型](https://github.com/THUDM/ChatGLM-6B)时使用的部分脚本，各个脚本的用途如下：

* `api_stream.py` 用于提供基于流式输出的 API 界面
* `fake_server.py`  提供一个调试用的服务器，模拟 ChatGLM 模型的输出
* `cmd-api.py` 测试原始 API 界面的脚本
* `cmd-stream.py` 测试流式输出接口的脚本
* `api_proxy.py` 用于在多个 ChatGLM 后端进行调度的脚本，可以提高前端同时服务人数

## 前端部署

前端使用了[chatglm-web 项目](https://github.com/NCZkevin/chatglm-web)，仅做了一点修改：原代码使用 `data: ` 作为数据的分割字符串，这里换成了`<^>`，不太容易冲突。

使用 nginx 部署的时候需要设置反向代理：

```
    location /api/ {
    proxy_pass http://localhost:3002/;
    proxy_buffering off;
}
```

## 后端部署

后端使用 `api_proxy.py` 作为代理，需要提供一个配置文件 `servers.txt`，里面包含提供 ChatGLM 服务的地址和端口，例如：
```
127.0.0.1:3003
127.0.0.1:3004
....
```
如果后台有 N 个 ChatGLM 实例，建议 `api_proxy.py` 可以设置 N+1 个 workers，例如：
```Shell
$ nvicorn api_proxy:app --host 127.0.0.1 --port 3002 --workers 8
```
对于 ChatGLM 服务的启动，在 `api_stream.py` 中设置使用的 GPU 数目是 2 个，可以根据实际情况进行调整。启动服务的命令可以类似如下（要在 ChatGLM-6B 目录中运行)：

```Shell
$ CUDA_VISIBLE_DEVICES=0,1 nvicorn api_stream:app --host 127.0.0.1 --port 3003
$ CUDA_VISIBLE_DEVICES=2,3 nvicorn api_stream:app --host 127.0.0.1 --port 3004
```
