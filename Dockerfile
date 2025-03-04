FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
  && apt-get install -y gcc libpq-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/\*

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

COPY . .

RUN mkdir -p /app/static && chmod -R 755 /app/static

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]