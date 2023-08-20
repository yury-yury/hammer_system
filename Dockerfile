FROM python:3.10-slim

EXPOSE 8000

ENV HOME /hammer_system_2

WORKDIR $HOME

COPY requirements.txt .
RUN python3 -m pip install --no-cache -r requirements.txt

ENV DB_HOST="localhost"
ENV DB_PORT="5432"

COPY . .

CMD python3 manage.py runserver 0.0.0.0:8000