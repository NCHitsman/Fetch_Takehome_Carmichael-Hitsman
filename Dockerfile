FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-u", "receipt-api.py"]
# This commented out ENTRYPOINT will start the container but not
# the python program. I have found this useful for debugging
# ENTRYPOINT ["tail", "-f", "/dev/null"]
