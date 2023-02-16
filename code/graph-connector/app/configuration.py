import os

KG_HOSTNAME = "http://disco-kg:3030/ds"

if os.getenv("GRAPH_CONNECTOR_DEBUG") == "true":
    print("Running in debug mode.")
    KG_HOSTNAME = "http://localhost:3030/ds"

if os.getenv("GRAPH_CONNECTOR_DEBUG") == "true":