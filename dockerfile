FROM python:latest

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

COPY . /app/

RUN python -m pip install --upgrade pip

RUN python -m pip install -r requirements.txt

CMD ["python", "app.py"]
