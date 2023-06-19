FROM python:3.10

WORKDIR /home/app/swipe

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install psycopg2 dependencies
RUN apt-get update && apt-get -y install gcc python3-dev musl-dev

RUN pip install --upgrade pip
# copy project
COPY . /home/app/swipe
RUN apt update
RUN pip install -r requirements.txt
RUN chmod a+x /home/app/swipe/init_entrypoint.sh
ENTRYPOINT ["/home/app/swipe/init_entrypoint.sh"]