FROM python:3.9.17-bullseye 

RUN pip install --upgrade pip

COPY ./sensor_api /opt/sensor_api
WORKDIR /opt/sensor_api
RUN pip install -r requirements.txt

WORKDIR /opt/sensor_api
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--preload", "-w", "4", "wsgi:app"]

EXPOSE 8000
