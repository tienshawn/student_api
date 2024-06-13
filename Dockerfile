FROM python:3.10-slim

WORKDIR /api

COPY requirements.txt app.py requirements.txt  /api/

RUN pip install --no-cache-dir -r /api/requirements.txt

ENV PORT 5000

EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
