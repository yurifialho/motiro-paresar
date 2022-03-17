FROM python:3.9

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /usr/src/app

COPY . /usr/src/app/.

CMD [ "python", "main.py"]