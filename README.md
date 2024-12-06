# ASSISTANT Visualization with ReactJS

## Contents

1. [Introduction](#1-introduction)
2. [User Interface](#2-user-interface)
3. [Backend with Flask](#3-backend-with-flask)
4. [Chatbot with rasa](#4-chatbot-with-rasa)
5. [Server Migration](#5-server-migration)
6. [Error Handling](#6-error-handling)

## 1. Introduction

This project contains the visualization of the Process Manager for automated process planning. The app is splitted in 
user interface, models and shaders.

The following guide is for development purposes only. It is ment to be run locally on your PC.

## 2. User Interface

The user interface enables the use of different backend functionalities sitting in the backend.

### Installation

Make sure you have Node.js and npm installed. A guide for all operating systems can be found [here](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
After installing Node.js and npm, go to the *user-interface* directory that includes the **package.json** file.
Run 
    npm install

to install all necessary dependencies for the project. This can be done everytime the project is pulled


### Starting App

In the directory *user-interface* run the following command to start the server:

    npm start


## 3. Backend with Flask

### Installation

Flask runs via Python and can be installed via pip. We recommend setting up a virtual environment.
Inside your python environment, navigate to the *backend* directory where the **setup.py** file is located.
Install all necessary packages via:

    pip install -e .

This is necessary as the flask requires the directory to be set up as a python package.

### Starting the Backend Server

To start the server, navigate to the backend package that contains the **.flaskenv** file and run:

    flask run


## 4. Chatbot with rasa

We use a rasa webchat to enable communication against the running ontologie with given responses.

### Installation

rasa runs via Python and can be installed via pip. We recommend setting up a virtual environment with Python 3.7 or 3.8.
All necessary packages can be installed via the **requirements.txt** file. Navigate to that file inside the *chatbot*
directory and run:

    pip install -r requirements.txt

### Starting the chatbot server

For the chatbot you need to run a rasa server to use the chatbot and an additional action server to query the ontology 
through the chatbot. 

To start the action server open a command window, activate the python environment and navigate to 
the *Chatbot3.0* directory. Start the server by running

    rasa run actions

Open a separate command window with the same environment and directory and run 

    rasa run -m models --enable-api --cors "*"

to start the rasa server.

### Changing the ontologie

A description of how to change the ontologie can be found within the [ReadMe](chatbot/README.md) inside the *chatbot* directory.


## 5. Server Migration

Currently all docker containers are uploaded to the Container registry manually and pulled onto the server due to issues
with docker-compose. The section describes helpful tips and code lines to upload the webservice.

### 1. Start database

The database is a postgresql database inside a docker container. To start the database run the following commands:

```
docker run -itd -e POSTGRES_USER=assistant -e POSTGRES_PASSWORD=0000 -p 5432:5432  


```

## 6. Error Handling

There is a difference between running the application locally and running them in a docker container. The following 
section describes problems that occurred during testing and should help to prevent similar mistakes from happening.

### Proxying
The frontend uses a proxy to connect to the backend. Locally, this url is *http://127.0.0.1:5000*. When having the 
frontend inside a docker container the proxy has to lead to the IP Address of the backend given by the docker bridge 
(check [here](https://www.tutorialworks.com/container-networking/) for further information). 

You can check the IP Address of a running container with 

```
docker inspect >containter-id< | grep IPAddress
```

The same procedure is also necessary to connect the backend to the database
### Changes to the database model

In case there are changes in the database models (not the content) it is necessary to upgrade the database using flask. 
It may be necessary to enter the backend container and reconfiguring the database:

```
docker exec -it <container-id> bash
(inside bash)
rm -R backend/migrations
flask --app backend/app.py db init
flask --app backend/app.py db migrate
flask --app backend/app.py db upgrade

```

This should update the database models. It is best to restart the container after update to ensure the backend 
application is running properly.
