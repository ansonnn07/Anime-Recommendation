FROM python:3.7

ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY requirements.txt /code/
# Install packages before copying the rest of the files
#  to reduce successive build times after installation is cached
RUN pip install -r requirements.txt
COPY . /code/

# CMD python main.py
CMD gunicorn --bind 0.0.0.0:5000 -w 3 main:app