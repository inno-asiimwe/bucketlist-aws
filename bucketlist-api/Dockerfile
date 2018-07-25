# Use an official Python runtime as a parent image
FROM python:3.6-slim

# set the working directory to /app
WORKDIR /app

# install netcat
RUN apt-get update && apt-get install -y netcat

# copy the requirements into the container at /app
ADD ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
ADD . /app

# Make port 5000 available to the world outside this container
# EXPOSE 5000

# #Define Environment variable
# ENV APP_SETTINGS production
# ENV SECRET My-secret-a-long-string
# ENV DBHOST flaskpsql.postgres.database.azure.com
# ENV DBUSER flaskpsqluser@flaskpsql
# ENV DBNAME flask_api
# ENV DBPASS cHr0m3.2013
# ENV FLASK_APP run.py

# Run run.py when the container launches, this is app entry point
CMD  [ "./entrypoint.sh"]