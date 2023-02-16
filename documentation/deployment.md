# Deploying disco-graph

disco-graph can be easily deployed using docker containers. On Linux or MacOS you can use the disco-graph.bash bash script
to follow this guide and be up and running in no time.

**Table of contents:**
1. [Prerequisites](#1-prerequisites)
2. [Start in 1 command](#2-start-in-1-command)
3. [Stop disco-graph](#3-stop-disco-graph)
4. [Building the Images](#4-building-the-images)
5. [Production Use](#5-production-use)
6. [How does the deployment work?](#6-how-does-the-deployment-work)
   1. [Knowledge Graph](#61-knowledge-graph)
   2. [graph-connector](#62-graph-connector)
   3. [ui](#63-ui)
7. [Deploying on Windows](#7-deploying-on-windows)
   1. [Creating the Network](#71-creating-the-network)
   2. [Starting the Containers](#72-starting-the-containers)

## 1. Prerequisites
To build and deploy disco-graph [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/)
are needed.

## 2. Start in 1 command
Using the shell ("Terminal" app) navigate to the [deploy/docker directory](../deploy/docker) and run the following command:
```shell
bash disco-graph.bash start
```
This will trigger all container images being build and started afterwards in a docker-compose deployment.
The webapp can be accessed by navigating to http://localhost in an internet browser.

## 3. Stop disco-graph
From the [deploy/docker directory](../deploy/docker) run the following command:
```shell
bash disco-graph.bash stop
```

## 4. Building the Images
From the [deploy/docker directory](../deploy/docker) run the following command:
```shell
bash disco-graph.bash build all
```
When successful this command will build docker images for all 3 components of disco-graph.

## 5. Production Use
Before using the docker images for a production deployment make sure to set a secure secret token for the graph-connector
deployment. To set the token you have to modify the [docker-compose.yml](../deploy/docker/graph-connector/docker-compose.yml) 
for the graph-connector.
```yaml
version: "3.9"
services:
  graph-connector:
    ...
    environment:
      - SECRET_TOKEN=change_to_secure_token
    ...
```
> Note: Make sure to change the secret token to a secure value when deploying the production version. To create a secure
> token you can run the following command to generate a 128 character token (requires [openssl](https://www.openssl.org/)):
> ```bash
> openssl rand -base64 128
> ```

## 6. How does the deployment work?
There are mainly two different parts that constitute the inner workings of the deployment: 
1. Dockerfiles that describe how an image is build. There is a Dockerfile for all 3 components [kg](../deploy/docker/fuseki/Dockerfile)
, [graph-connector](../code/graph-connector/Dockerfile) and [ui](../code/disco-graph/ui/Dockerfile). Read the 
[official documentation](https://docs.docker.com/engine/reference/builder/) for an in depth explanation of Dockerfiles.
2. docker-compose.yml files that describe how container images should be deployed, again for [kg](../deploy/docker/fuseki/docker-compose.yml)
, [graph-connector](../deploy/docker/graph-connector/docker-compose.yml) and [ui](../deploy/docker/ui/docker-compose.yml).
See the [official documentation](https://docs.docker.com/compose/features-uses/) for more info.

### 6.1. knowledge-graph
The knowledge graph uses the [fuseki docker image](https://jena.apache.org/documentation/fuseki2/fuseki-docker.html), which
is a SPARQL server based on Apache Jena.

### 6.2. graph-connector
Taking a look at the [Dockerfile](../code/graph-connector/Dockerfile) you can see that the application is launched using
the [gunicorn](https://gunicorn.org/) WSGI HTTP server. This is done because the inbuilt server of flask is not supposed 
to be used in a production setting. The gunicorn server is configured in the [gunicorn.conf.py](../deploy/docker/graph-connector/gunicorn.conf.py) 
file. 

### 6.3. ui
Looking at the [Dockerfile](../code/disco-graph/ui/Dockerfile) you see a build process that is split into two parts. First
the application is build and the output of this step is then given to the second step where an image utilizing the [NGINX](https://www.nginx.com/)
web server is build. This server is used as single point of entry for web traffic, serving the ui and acting as reverse 
proxy to the graph-connector. It is configured in the [nginx.conf](../code/disco-graph/ui/nginx.conf) file.

## 7. Deploying on Windows
> TODO
### 7.1. Creating the Network

### 7.2. Starting the Containers