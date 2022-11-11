FROM python:3.10
COPY app/* /home/app/
COPY requirements.txt /home/
WORKDIR /home
RUN pip install -r requirements.txt
ENTRYPOINT FLASK_APP=app/app.py flask run --host=0.0.0.0