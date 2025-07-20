FROM python:slim

WORKDIR /app

COPY requirements.txt .

COPY alert-router.py .

RUN pip install -r requirements.txt

ENTRYPOINT [ "fastapi", "dev" ]

CMD [ "alert-router.py", "--host", "0.0.0.0" ]