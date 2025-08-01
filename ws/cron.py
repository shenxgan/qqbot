import os
import sys
import asyncio
import datetime
import importlib
import json
import traceback

from utils import get_files_hash

from sanic import Sanic
from sanic.log import logger


async def update_plugin_hash(app):
    """更新插件的哈希值，检测文件是否变动"""
    for k, v in app.ctx.plugins.items():
        new_hash = get_files_hash(f'plugins/{k}')
        if new_hash != v['hash']:
            logger.info(f'插件文件有变动，重新加载插件 {k}')
            module_name = f'plugins.{k}.main'
            module = sys.modules[module_name]
            # x = importlib.import_module(f'plugins.{k}.main')
            x = importlib.reload(module)  # 有缓存，必须重新加载
            app.ctx.plugins[k]['instance'] = x.Plugin()
            app.ctx.plugins[k]['hash'] = new_hash


async def load_new_plugins(app):
    """自动加载新的插件"""
    for de in os.scandir('plugins'):
        if not de.is_dir():
            continue
        if de.name == '__pycache__':
            continue
        if de.name in app.ctx.plugins:
            continue
        try:
            logger.info(f'加载插件 {de.name}')
            x = importlib.import_module(f'plugins.{de.name}.main')
            app.ctx.plugins[de.name] = {
                'instance': x.Plugin(),
                'hash': get_files_hash(f'plugins/{de.name}'),
            }
        except Exception as e:
            logger.error(f'插件 {de.name} 加载失败：{e}')


async def cron(app, now):
    """定时任务，每次运行所有定时任务插件"""
    ws = app.ctx.ws

    for k, v in app.ctx.plugins.items():
        plugin = v['instance']
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
            await update_plugin_hash(app)
            await load_new_plugins(app)
        await asyncio.sleep(1)
