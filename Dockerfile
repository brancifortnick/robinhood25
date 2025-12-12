FROM node:17 AS build-stage

WORKDIR /react-app
COPY react-app/. .


ENV REACT_APP_BASE_URL=https://robin-hood-clone-74aef86e2cd5.herokuapp.com/

RUN npm install
RUN npm run build

FROM python:3.9


ENV FLASK_APP=app
ENV FLASK_ENV=production
ENV SQLALCHEMY_ECHO=True

EXPOSE 8000

WORKDIR /var/www
COPY . .
COPY --from=build-stage /react-app/build/* app/static/


RUN pip install -r requirements.txt
RUN pip install psycopg2

RUN flask environment
CMD gunicorn app:app
