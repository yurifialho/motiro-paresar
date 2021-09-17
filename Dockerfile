FROM python:3


COPY . /home/planneragent/.
WORKDIR /home/planneragent
RUN python -m pip install -r requirements.txt

CMD [ "python", "main.py"]