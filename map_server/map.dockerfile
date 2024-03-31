FROM python:3.9.17-bullseye 

RUN pip install --upgrade pip

COPY ./map_server/ /opt/map_server
WORKDIR /opt/map_server
RUN pip install -r requirements.txt

WORKDIR /opt/map_server
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--preload", "-w", "4", "wsgi:app"]

EXPOSE 8000
