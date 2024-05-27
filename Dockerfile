FROM python:3.10-slim

WORKDIR /api

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "app:application", "-b", "0.0.0.0:5000", "-w", "4"]