# disco graph
Knowledge graph powered information discovery based on keyword associations.

## Deployment
disco-graph can be deployed with a single command on Linux and MacOS if docker and docker-compose are installed:\
Using the shell navigate to the [deploy/docker directory](../deploy/docker) and run the following command:
```shell
bash disco-graph.bash start
```
To stop it run:
```shell
bash disco-graph.bash stop
```
A more in depth description of the deployment can be found in the **[Deployment Guide](documentation/deployment.md)**.

## Setting up development environment
The **[Development Guide](documentation/development.md)** details how to set up your machine to contribute to disco-graph.

## General Information
The disco graph application consists of three major components: The Knowledge Graph, the Backend services and the 
Frontend. A short description of these components is given in the following paragraphs. For a more in-depth description
take a look at the guides to each if the individual components:

[Knowledge Graph](documentation/components/knowledge-graph.md)\
[graph-connector](documentation/components/graph-connector.md)\
[UI](documentation/components/disco-graph-ui.md)

### Knowledge Graph
The Knowledge Graph is the heart of Disco Graph, as it serves as main data-structure containing the relationships
between Publications, Keywords and further information. This datastructure allows for efficient retrieval of relevant
information. The Knowledge Graph is accessed through the Backend. The Knowledge Graph consists of RDF triples that are
stored in an [Apache Jena Fuseki SPARQL Server](https://jena.apache.org/documentation/fuseki2/).

### Frontend
The Frontend allows users to discover the knowledge hidden in the knowledge graph. It combines features to search, view
and edit information about publications and provides an interface for managing users and roles through the admin portal.

The Frontend is a webapp based on the [Angular Framework](https://angular.io/), using the [Angular Material component 
library](https://material.angular.io/).

### Backend
The backend acts as link between Frontend and Knowledge Graph and provides additional features like user management and 
roles. \
The Backend is a [Flask application](https://flask.palletsprojects.com/en/2.2.x/) that uses 
[rdflib](https://rdflib.readthedocs.io/) to interface with the knowledge graph.


## API
Take a look at the [graph-connector API documentation](./documentation/api.md) to get insights into how and with what data to use the backend api.