FROM python:3.10.6
WORKDIR /proyecto
COPY API API
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn API.app:app --host 0.0.0.0 --port $PORT
