FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "itraxcn.wsgi:application"]
