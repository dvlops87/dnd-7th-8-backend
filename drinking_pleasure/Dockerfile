FROM python:3.8

ENV PYTHONUNBUFFERED 1
WORKDIR /dnd-7th-8-backend/drinking_pleasure
COPY . .

RUN sudo pip install --upgrade pip
RUN sudo pip install -r requirements.txt

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000