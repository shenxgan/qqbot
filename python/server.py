import asyncio
import os
import time

from sanic import Sanic
from sanic import text
from sanic.log import logger

app = Sanic('python')


cmds = {
    'py': 'timeout {timeout} python -u {fname}',
    'c': 'timeout {timeout} gcc -x c -o {fname}.o {fname}'
         ' && timeout {timeout} {fname}.o',
    'js': 'timeout {timeout} node {fname}',
}


def check_language(code):
    """检测代码语言"""
    tp = 'py'
    if '#include <stdio.h>' in code:
        tp = 'c'
    elif 'console.log' in code:
        tp = 'js'
    logger.info(f'代码语言为：{tp}')
    return tp


@app.post('/code')
async def run_code(request):
    """运行代码
    保存为文件后执行，并设置超时时间（5秒）
    """
    data = request.json
    code = data['code']

    timeout = 1
    max_line = 15
    max_len = 256

    now = time.time()
    fname = f'/tmp/{now}'
    with open(fname, 'w') as f:
        f.write(code)

    tp = check_language(code)
    cmd = cmds[tp].format(timeout=timeout, fname=fname)
    logger.info(cmd)
    proc = await asyncio.create_subprocess_shell(
        f'su work -c "{cmd}"',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    for i in range(9):
        try:
            msg = stdout[:max_len+i].decode() + stderr[:max_len+i].decode()
            break
        except Exception:
            pass
    os.remove(fname)

    _msg = msg.split('\n')[:max_line]
    res = '\n'.join(_msg)[:max_len]
    return text(res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=False, auto_reload=True)
