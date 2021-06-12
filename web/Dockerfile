FROM python:3.7

ENV PYTHONUNBUFFERED 1
# Remove this env variable when deploying with Heroku
ENV PORT=5000

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
# Install packages before copying the rest of the files
#  to reduce successive build times after installation is cached
RUN pip install -r requirements.txt
COPY . /code/

# If using Heroku, must use Heroku's own PORT env variable
CMD gunicorn --bind 0.0.0.0:$PORT -w 3 main:app