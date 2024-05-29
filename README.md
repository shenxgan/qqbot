## 介绍
- 使用的是 [Lagrange.OneBot](https://github.com/LagrangeDev/Lagrange.Core)
- 开箱即用，使用 docker 一键启动

## 首次启动
```bash
docker compose up
```

然后扫码登录即可，会登录到 linux 平台

## 测试
- 进群发送 python 即可看到回复
- 所有关键字以及自动回复的消息均存于 [`ws/botmsg.txt`](ws/botmsg.txt) 文件中
- 修改了 `ws/botmsg.txt` 文件后需要重启

## 后台启动
```bash
docker compose up -d
```

## 配置文件
- 配置文件是 [`data/appsettings.json`](data/appsettings.json)

## 添加自己的回复逻辑
- 我们使用的是反向 websocket
- 逻辑代码位于 [`ws/server.py`](ws/server.py) 文件
