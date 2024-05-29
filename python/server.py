import asyncio
import datetime

from sanic import Sanic
from sanic import text

app = Sanic('python')


@app.post('/code')
async def run_code(request):
    """运行代码
    保存为文件后执行，并设置超时时间（5秒）
    """
    data = request.json
    code = data['code']
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    fname = f'/tmp/{now}.py'
    with open(fname, 'w') as f:
        f.write(code)
    cmd = f'timeout 5 python {fname}'
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    msg = stdout.decode() + stderr.decode()

    _msg = msg.split('\n')[:15]
    res = '\n'.join(_msg)
    return text(res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=False, auto_reload=True)
