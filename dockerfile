FROM python:3.10.7

WORKDIR /

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./main.py ./main.py

CMD ["python", "./main.py"]