FROM python

COPY ./requirements.txt /app/requirements.txt
COPY ./app /app
COPY ./main.py /app/
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


CMD ["uvicorn","app.main:app","--host","0.0.0.0", "--port","80"]

