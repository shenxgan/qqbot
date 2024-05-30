FROM python:3.12-slim

RUN useradd -m work

WORKDIR /app

COPY requirements.txt server.py /app/
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

USER work

CMD ["python", "server.py"]
