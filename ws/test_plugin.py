import asyncio
import sys
import importlib

"""
插件功能测试，仅支持部分简单的插件
只有没有使用 app、ws 等属性的插件才能运行此脚本进行测试
此脚本需要两个参数：
    1. {name} 插件名称
    2. {message} 内容
运行示例：
    python test_plugin.py idiom "一心一意"
"""


async def main():
    name = sys.argv[1]
    message = sys.argv[2]

    x = importlib.import_module(f'plugins.{name}.main')
    plugin = x.Plugin()

    ws = None
    data = {}
    ats = set()
    for attr in {'ws', 'data', 'ats'}:
        if hasattr(plugin, attr):
            setattr(plugin, attr, locals()[attr])
    msg = await plugin.run(message)
    print(msg)


asyncio.run(main())
