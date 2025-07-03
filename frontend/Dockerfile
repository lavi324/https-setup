FROM python:3.10-slim

WORKDIR /app

RUN pip install flask gunicorn

COPY . /app

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
