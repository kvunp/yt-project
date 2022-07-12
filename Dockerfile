FROM python:3.7-slim

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

EXPOSE 5000:5000

COPY requirements.txt .

RUN pip3 install -r requirements.txt

ADD . .

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "5000"]