# Chessmaistro - Docker 

This app is built with Dash, a Python framework to build elegant interactive dashboards for the web. 
We also use a template to create a Docker image that uses Flask, Nginx, and uWSGI to serve the application.

This app will basically take your chess.com username, and a few extra parameters, 
and show you:

- some statistics about your game, taking daily rating as the maximum rating achieved.
This promotes the users to keep playing once they broke their record or got a high elo.

- A personalized news generator:  depending on how 
you performed yesterday on chess.com, you will have a
news article about you.
It is meant to be written in a sensationalistic way, either idolizing or demonizing you
according to your performance.

## Dockerize your Dash app

1. Create Docker image
```
docker build -t my_dashboard .
```

2. Run app in container
```
docker run -p 8080:80 my_dashboard
```
This will run the app on http://localhost:8080/.

The base image used in the Dockerfile: https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/. 