FROM python:3.7

WORKDIR /API_DOCKER

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

RUN export PYTHONPATH='${PYTHONPATH}:/API_DOCKER'

COPY . .

CMD ["python", "./run.py"]