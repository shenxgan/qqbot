import re
import secrets
import string
import subprocess


"""
随机文章名称
使用4位随机数字组成，名称全局唯一
"""


def get_current_codes():
    config_file = '.vitepress/config.mjs'
    with open(config_file) as f:
        data = f.read()

    codes = re.findall(r"\{ text: '.*?', link: '/.*?/(\d{4})' \}", data)
    return codes


def get_current_all_codes():
    cmd = "find ./ -name '*.md' -not -path './node_modules/*'"
    res = subprocess.run(
        cmd, capture_output=True, shell=True,
        check=True, encoding='utf-8')
    codes = re.findall(r'.*(\d{4})\.md', res.stdout)
    print('总共：', len(codes))
    return codes


def random_code():
    return ''.join(secrets.choice(string.digits) for i in range(4))


def new_code(codes):
    while True:
        code = random_code()
        if code not in codes:
            print(code)
            break


if __name__ == '__main__':
    codes = get_current_all_codes()
    for i in range(5):
        new_code(codes)
