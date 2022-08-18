FROM python:latest

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN python -m pip install --upgrade pip

RUN python -m pip install -r requirements.txt

COPY . /app/

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]

