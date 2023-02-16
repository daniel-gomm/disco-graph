# Example Jupyter Notebooks

In the [example/notebooks](../example/notebooks) folder you can find different jupyter notebooks demonstrating different 
aspects of using disco-graph. Additionally, example data is provided.\
To use these notebooks open them with the [jupyter computing platform](https://jupyter.org/).

## Add Admin User
To register an admin user you can use the [Add Admin User notebook](../example/notebooks/Add%20admin%20user.ipynb). All
the necessary steps are detailed there. Make sure to have the secret token ready as it is necessary to authenticate the
creation of an admin user. It can be set as environment variable in the 
[docker-compose run configuration](../deploy/docker/graph-connector/docker-compose.yml) for the graph-connector service. 
The development version has the secret token "debug".
> Note: Make sure to change the secret token to a secure value when deploying the production version. To create a secure
> token you can run the following command to generate a 128 character token (requires [openssl](https://www.openssl.org/)):
> ```bash
> openssl rand -base64 128
> ```

## Load Example Publications
The [Load Example Publications notebook](../example/notebooks/Load%20Example%20Publications.ipynb) provides a blueprint
for loading data into the knowledge graph. Make sure to set up an admin account first, as it is needed to add publications.