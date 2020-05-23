FROM python:3.6

RUN mkdir -p /app/
WORKDIR /app/

COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt

ENV TZ=UTC
ENV PYTHONUNBUFFERED=1