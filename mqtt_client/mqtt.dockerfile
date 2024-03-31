FROM python:3.9.17-bullseye 

RUN pip install --upgrade pip

COPY ./mqtt_client /opt/mqtt_client
WORKDIR /opt/mqtt_client
RUN pip install -r requirements.txt

WORKDIR /opt/mqtt_client
CMD ["python3", "-u", "main.py"] 
