# Development Setup

This document describes how to set up the development environment to develop the components of
disco-graph. To work on the graph-connector backend one needs to set up a python development environment. To work on the
ui one needs to set up angular.

When debugging the application all components have to interact with each other, therefore it is necessary to spin up all
3 components of the system. How to do that is elaborated upon at the end of this document.

**Table of Contents:**
1. [Python environment - graph-connector](#python-environment---graph-connector)
   1. [Installing Dependencies](#installing-dependencies)
   2. [Opening project in IDE](#opening-project-in-ide)
   3. [Running and debugging from the IDE](#running-and-debugging-from-the-ide)
   4. [Running from the shell](#running-from-the-shell)
2. [Angular setup](#angular-setup)
   1. [Installing Angular](#installing-angular)
   2. [Installing Dependencies](#installing-dependencies-1)
   3. [Opening project in IDE](#opening-project-in-ide-1)
   4. [Running the application](#running-the-application)
   5. [Debugging](#debugging)
3. [Testing the application](#testing-the-application)
   1. [Starting the knowledge-graph](#starting-the-knowledge-graph)
   2. [Starting other components as development docker-containers](#starting-other-components-as-development-docker-containers)
   3. [General debugging workflow](#general-debugging-workflow)
   4. [Loading sample data into the Knowledge Graph](#loading-sample-data-into-the-knowledge-graph)
   5. [Initializing users and admins](#initializing-users-and-admins)

## Python environment - graph-connector
Prerequisites: Working installation of Python 3.10 and pip (for example using [Anaconda](https://www.anaconda.com/)).

> _Note: Managing the python installation and installed packages is easier when using virtual environments. You can read
> up on virtual environments [here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)_ 

### Installing Dependencies 
From the [graph-connector directory](../code/graph-connector) execute the following command in a shell:
```shell
pip install -r requirements.txt
```
This will fetch and install all the relevant dependencies used in graph-connector.

### Opening project in IDE
Use the IDE of your choice and open the repository. The graph-connector code is found in the [code/graph-connector](../code/graph-connector)
directory. Graph-connector is a RESTful Application based on the [flask framework](https://flask.palletsprojects.com/).
To get started with flask have a look at the [official tutorial](https://flask.palletsprojects.com/en/2.2.x/tutorial/).

### Running and debugging from the IDE
To run the application from an IDE an appropriate run configuration has to be used.
Make the following settings in the run configuration:
1. Add the environment variable `GRAPH_CONNECTOR_DEBUG=true`
2. Provide the arguments `--no-reload --without-threads` as parameters. This allows for straight forward debugging because
everything is executed in a single thread.



> This is what the run configuration looks like in the [PyCharm IDE](https://www.jetbrains.com/pycharm/).
>![graph-connector_run_configuration.png](resources/graph-connector_run_configuration_pycharm.png)
> And this is what it looks line in [Visual Studio Code](https://code.visualstudio.com/)
> ![graph-connector_run_configuration_vscode.png](resources%2Fgraph-connector_run_configuration_vscode.png)

### Running from the shell
To run the graph-connector application from the shell run the following command from the [code/graph-connector directory](../code/graph-connector):

Linux:
```shell
(export GRAPH_CONNECTOR_DEBUG=true ; flask --app app --debug run)
```

## Angular setup
### Installing Angular
To install Angular follow their [official documentation](https://angular.io/guide/setup-local).
The UI development is tested with Node 16.18.1, NPM 8.19.2 and Angular 15.0.0.

### Installing Dependencies
Navigate to the [code/disco-graph/ui directory](../code/disco-graph/ui) and run the following command:
```shell
npm install
```
This will install all the required dependencies.

### Opening project in IDE
Open the [code/disco-graph/ui directory](../code/disco-graph/ui) in the IDE of your choice (VS Code works great).
The disco-graph ui is a web application based on the [Angular framework](https://angular.io/).

### Running the application
The application is run using the serve command:
```shell
ng serve
```

### Debugging
Debugging can be done either in the IDE or directly [in the browser](https://www.browserstack.com/guide/debug-angular-app-in-chrome) 
using the inbuild dev tools. These tools also allow you to set breakpoints in the code, similar to debugging in the IDE:
![debugging_dev_tools.png](resources%2Fdebugging_dev_tools.png)

## Testing the application
Since the components of disco-graph depend on each other you need to spin up the different components in order to test
each one of them.

### Starting the knowledge-graph
To start a development version of the knowledge-graph docker container the [disco-graph.bash](../deploy/docker/disco-graph.bash) 
can be used. To run the container execute the following command from the [deploy/docker directory](../deploy/docker):
```shell
bash disco-graph.bash start --dev kg
```
### Starting other components as development docker-containers
Using the script you can also start a development version of the graph-connector and the ui or any combination of the
components. The following command runs all 3 components in development mode:
```shell
bash disco-graph.bash start --dev kg gc ui
```

### General debugging workflow
Usually one would launch the development container of the knowledge graph and the other 2 components would be launched from 
the IDE. Depending on the specific use-case your milage may vary.

### Loading sample data into the Knowledge Graph
>_TODO: This is still an open point and has to be answered later_

### Initializing users and admins
>_TODO_