from flask import Flask, request
from markupsafe import escape
from model import publication

app = Flask(__name__)

#Max 25 mb content size (pdf size restriction)
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024

@app.post("/publication/<string:identifier>")
def add_publication(identifier, body):
     pub = publication(request)


