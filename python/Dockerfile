FROM python:3.12-slim

RUN useradd -m work

WORKDIR /app

COPY requirements.txt server.py /app/
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt \
    && sed -i 's#deb.debian.org#mirrors.tuna.tsinghua.edu.cn#g' /etc/apt/sources.list.d/debian.sources \
    && apt update && apt install -y gcc nodejs

CMD ["python", "server.py"]
