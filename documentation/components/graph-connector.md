# graph-connector

**Table of contents:**
1. [Overview](#1-overview)
2. [Code](#2-code)
   1. [Architecture](#21-architecture)
      1. [User Management](#211-user-management)
      2. [KG Interaction](#212-kg-interaction)
   2. [File Structure](#22-file-structure)
3. [Data Insertion](#3-data-insertion)
   1. [Insert Publications](#31-insert-publications)
   2. [Add Admins](#32-add-admins)


## 1. Overview
The graph-connector is the backbone of disco-graph. graph-connector is a RESTful application based on the 
[flask framework](https://flask.palletsprojects.com/). It serves 2 main purposes: Managing users and their access rights,
and accessing the knowledge graph. Therefore, it exposes endpoints to interact with all of these functionalities.
## 2. Code
The code for graph-connector is found in the [code/graph-connector directory](../../code/graph-connector).
### 2.1. Architecture
![graph-connector_architecture.png](..%2Fresources%2Fgraph-connector_architecture.png)
This depiction of the graph-connector shows a schema of the inner workings of graph-connector.\
To get a better understanding of how the different components work together we'll follow how a request is handled. Let's 
take the example of a request to modify a publication. This request would be first suspect to the authentication component,
which check if the user is logged in and has the appropriate rights. After this it is handled by the publication endpoint,
which in turn triggers the query engine to construct a query that undertakes the specified modifications.

#### 2.1.1. User Management
There are two categories of users: Admins and regular users. These roles are completely separate and serve different 
purposes. Users that are not logged in can also interact with the application with limited access.\
The privileges are as follows:

| Role          | Rights                                                                                                                                             |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| not logged in | - search the knowledge graph<br>- set search filters<br>- display search results and details                                                       |
| user          | Everything that can be done when not logged in +<br>- up-/down-vote keyword associations<br>- add keywords<br>- up-/down-vote additional attributes |
| admin         | Everything that can be done when not logged in +<br>- add and remove users<br>- add and remove publications                                        |

The login status of a user is saved in the users session and is checked for each request to a restricted resource.

#### 2.1.2. KG Interaction
The interaction with the knowledge graph is done using the [rdflib](https://rdflib.readthedocs.io/) library and SPARQL
queries. These queries are pre-formulated as templates. The templates are used by the query engine and populated with the
appropriate parameters.

### 2.2. File Structure
```text
📦graph-connector
 ┣ 📂app
 ┃ ┣ 📂model                         Contains data model definitions
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┗ 📜model.py                    Data model definitions
 ┃ ┣ 📂rdf                           Query templates and utilities for SPARQL queries
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜common.py                   Shared functions for query template definition    
 ┃ ┃ ┣ 📜document_queries.py         Query templates for queries aiming at publications
 ┃ ┃ ┣ 📜keyword_queries.py          Query templates for queries aiming at keywords
 ┃ ┃ ┗ 📜queries.py                  General query templates (e.g. search)
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜api_resource.py               Endpoint for search resources
 ┃ ┣ 📜auth.py                       Authentication logic
 ┃ ┣ 📜configuration.py              Configuration
 ┃ ┣ 📜db.py                         Defined interaction with SQL database
 ┃ ┣ 📜keyword_resource.py           Endpoint for keyword resources
 ┃ ┣ 📜publication_resource.py       Endpoint for publication resources
 ┃ ┣ 📜rdf_interface.py              Backbone of query engine, used to combine templates with data
 ┃ ┣ 📜request_utils.py              
 ┃ ┣ 📜schema.sql                    Definition of the sql schema for the user and admin tables
 ┃ ┗ 📜user_resource.py              Endpoint for user/admin resources
 ┣ 📜Dockerfile                      Defines how the docker container is build
 ┣ 📜MANIFEST.in
 ┣ 📜__init__.py
 ┣ 📜requirements.txt
 ┗ 📜setup.py
```

## 3. Data Insertion

### 3.1. Insert Publications
For how to insert publications take a look at the [documentation on the provided example notebook](../notebooks.md#load-example-publications).

### 3.2. Add Admins
For how to add admins take a look at the [documentation on the provided example notebook](../notebooks.md#add-admin-user).