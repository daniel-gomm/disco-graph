FROM python:3.10
COPY . /home/graph-connector/
COPY . /home/graph-connector/
WORKDIR /home/graph-connector
RUN pip install -r  requirements.txt
RUN mkdir /home/graph-connector/instance
RUN echo SECRET_KEY = \'$(python -c 'import secrets; print(secrets.token_hex())')\' > /home/graph-connector/instance/config.py
#ENTRYPOINT flask --app app run --host=0.0.0.0
#ENTRYPOINT gunicorn --config /home/conf/gunicorn.conf.py --log-config /home/conf/gunicorn-logging.conf app:app
ENTRYPOINT gunicorn --config /home/conf/gunicorn.conf.py app:app