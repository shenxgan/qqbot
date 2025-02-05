import asyncio
import datetime
import json
import traceback

from sanic import Sanic
from sanic.log import logger


async def cron(app, now):
    """定时任务，每次运行所有定时任务插件"""
    ws = app.ctx.ws

    for plugin in app.ctx.plugins:
        if plugin.type != 'cron':
            continue
        plugin.is_at = False
        try:
            msg = await plugin.run(now)
            if not msg:
                continue
            for group_id in plugin.group_ids:
                ret = {
                    'action': 'send_group_msg',
                    'params': {
                        'group_id': group_id,
                        'message': msg,
                    }
                }
                await ws.send(json.dumps(ret))
        except Exception as e:
            logger.error(f'插件 {plugin} 运行报错：{e}')
            logger.error(traceback.format_exc())


async def cron_job():
    """时刻运行，每分钟检测一次定时任务"""
    app = Sanic.get_app()
    flag = False
    while True:
        if flag is False:
            logger.info('定时任务启动，应只启动一次，多次就是有误')
            flag = True
        now = datetime.datetime.now()
        if now.second == 0:
            if now.minute == 0:
                logger.info(f'整点报时：{now}')
            await cron(app, now)
        await asyncio.sleep(1)
