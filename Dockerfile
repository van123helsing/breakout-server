FROM python:3.6-slim-buster
COPY breakout-server /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8443
CMD python ./main.py