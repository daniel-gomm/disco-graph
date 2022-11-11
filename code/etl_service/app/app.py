from flask import Flask, request
from model import Publication
from rdf_interface import RDFConnector

app = Flask(__name__)

# Max 25 mb content size (pdf size restriction)
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024

rdf_connector = RDFConnector("http://localhost:3030/ds")


@app.post("/publication/<string:identifier>")
def add_publication(identifier):
    req_json = request.get_json()
    pub = Publication(req_json)
    rdf_connector.add_to_graph(pub)
    app.logger.info(f"Successfully added new publication {pub.pub_id}")
    return f"Sucessfully added new publication {pub.pub_id}"


if __name__ == "__main__":
    app.run()
