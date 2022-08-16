FROM python:3.8

ENV PYTHONUNBUFFERED 1

# 도커 컨테이너 내에서 코드가 실행될 경로 설정
RUN mkdir /code
WORKDIR /code

# 코드 실행될 경로에 requirments.txt 복사 후 설치
ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 프로젝트를 code로 복사
ADD . /code/
