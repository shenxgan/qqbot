# Python 学习机器人

## 介绍
- 使用的是 [Lagrange.OneBot](https://github.com/LagrangeDev/Lagrange.Core)
- 开箱即用，使用 docker 一键启动

## 功能
- 关键字触发回复（关键字均与 python 相关）
- 运行代码（支持 python/c/javascript 代码）并回复执行输出

## 首次启动
```bash
docker compose up
```

然后扫码登录即可，会登录到 linux 平台

## 测试
- 进群发送 python 即可看到回复
- 所有关键字以及自动回复的消息均存于 [`ws/plugins/kv_python/kvmsg.txt`](ws/plugins/kv_python/kvmsg.txt) 文件中
- 修改了 `ws/plugins/kv_python/kvmsg.txt` 文件后需要重启
    ```bash
    docker compose down
    docker compose up --build
    ```

## 后台运行
```bash
docker compose up -d
```

## 配置文件
- 配置文件是 [`bot/appsettings.json`](bot/appsettings.json)

## 添加自己的回复逻辑
- 我们使用的是反向 websocket
- 逻辑代码位于 [`ws/server.py`](ws/server.py) 文件

## 切换QQ账号
- 删掉 bot 目录下除了 `appsettings.json` 之外的所有文件
- 重新启动，使用新QQ扫码登录即可
