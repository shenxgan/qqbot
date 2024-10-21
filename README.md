# Python 学习机器人

## 介绍
- 可选用 [Lagrange.OneBot](https://github.com/LagrangeDev/Lagrange.Core) 或 [NapCatQQ.OneBot](https://github.com/NapNeko/NapCat-Docker)
- 开箱即用，使用 docker 一键启动

## 首次启动
```bash
# 使用 lagrange 协议，也可选择 napcat 协议
docker compose --profile lagrange up
```

然后扫码登录即可，会登录到 linux 平台

## 后台运行
```bash
docker compose --profile lagrange up -d
```
