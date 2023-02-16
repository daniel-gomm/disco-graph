#!/bin/bash

cli_name=${0##*/}
RED='\033[0;31m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
NC='\033[0m'

create_network() {
  # create docker network if it does not exist
  docker network inspect disco-graph >/dev/null 2>&1 || \
  ( echo "Network does not exist, creating disco-graph network..." ; docker network create disco-graph )
}

start_production() {
  echo "Deploying images..."
  create_network

  if [ "$( docker images | grep fuseki | wc -l)" -gt 0 ]; then
    echo "Image fuseki found locally."
  else
    build_kg_image
  fi
  echo "Starting knowledge graph..."
  docker-compose -f fuseki/docker-compose.yml up -d

  if [ "$( docker images | grep graph-connector | wc -l)" -gt 0 ]; then
    echo "Image graph-connector found locally."
  else
    build_graph_connector_image
  fi
  echo "Starting graph-connector (backend)..."
  docker-compose -f graph-connector/docker-compose.yml up -d

  if [ "$( docker images | grep disco-graph-ui | wc -l)" -gt 0 ]; then
    echo "Image disco-graph-ui found locally."
  else
    build_ui_image
  fi
  echo "Starting ui..."
  docker-compose -f ui/docker-compose.yml up -d
}

start_development() {
  echo "Deploying images in development mode..."

  if [[ "$*" == *" kg"* ]]; then
    echo "Starting knowledge graph..."
    docker-compose -f fuseki/docker-compose.dev.yml up -d
  fi

  if [[ "$*" == *" gc"* ]]; then
    echo "Starting graph-connector..."
    docker-compose -f graph-connector/docker-compose.dev.yml up -d
  fi

  if [[ "$*" == *" ui"* ]]; then
    echo "Starting ui..."
    docker-compose -f ui/docker-compose.dev.yml up -d
    echo -e "UI started on http://localhost:8080"
  fi

}

stop_production() {
  docker-compose -f ui/docker-compose.yml down
  docker-compose -f graph-connector/docker-compose.yml down
  docker-compose -f fuseki/docker-compose.yml down
}

stop_development() {
  docker-compose -f ui/docker-compose.dev.yml down
  docker-compose -f graph-connector/docker-compose.dev.yml down
  docker-compose -f fuseki/docker-compose.dev.yml down
}

build_image() {
  base_directory=$(pwd)
  cd "$1" || echo -e "${RED}Failed to locate $2 directory${NC}"
  echo "Building $2 image..."
  docker build . -t $3
  cd "$base_directory" || echo -e "${RED}Failed to locate $base_directory${NC}"
}

build_ui_image() {
  build_image ../../code/disco-graph/ui "ui" disco-graph-ui
}

build_graph_connector_image() {
  build_image ../../code/graph-connector "graph-connector" graph-connector
}

build_kg_image() {
  base_directory=$(pwd)
  cd ./fuseki || echo -e "${RED}Failed to locate disco-graph-kg directory${NC}"
  mkdir -p databases/DB2
  mkdir logs
  mkdir -p dev_databases/DB2
  mkdir dev_logs
  echo "Building disco-graph-kg image..."
  docker-compose build --build-arg JENA_VERSION=3.16.0
  cd "$base_directory" || echo -e "${RED}Failed to locate $base_directory${NC}"
}

show_dev_logs() {
  echo -e "${GREEN}Press Ctrl+C to exit logs"
  docker-compose -f $1/docker-compose.dev.yml logs -f
}

show_logs() {
  echo -e "${GREEN}Press Ctrl+C to exit logs"
  docker-compose -f $1/docker-compose.yml logs -f
}

clean() {
  docker network rm disco-graph
  docker image prune
}

show_help() {
  echo -e "
disco-graph deployment helper

The components of disco-graph are referenced by the following acronyms:
${GREEN}kg:${NC} knowledge graph
${GREEN}gc:${NC} graph-connector (backend)
${GREEN}ui:${NC} user interface (web app)

Usage: bash $cli_name ${CYAN}COMMAND${NC} ${GREEN}[OPTIONS]${NC}

${CYAN}Commands:${NC}   ${GREEN}Options:${NC}           Description:
  ${CYAN}build${NC}     ${GREEN}[all kg gc ui]${NC}     build specified docker images
  ${CYAN}start${NC}     ${GREEN}[--dev][kg gc ui]${NC}  start docker containers; in development mode the images to start need to be specified
  ${CYAN}stop${NC}      ${GREEN}[--dev]${NC}            stop the running docker containers
  ${CYAN}logs${NC}      ${GREEN}[--dev][kg gc ui]${NC}  show the logs of the specified container
  ${CYAN}help${NC}                         show this help page

Examples:
  bash $cli_name ${CYAN}start${NC} ${GREEN}--dev kg gc${NC}    Starts the knowledge graph and the graph-connector in development mode
  bash $cli_name ${CYAN}stop${NC}               Stops the production deployment of disco-graph
"
exit 1
}

show_logs_help() {
  echo -e "
${RED}Please specify the logs for which container you want to follow:${NC}
${CYAN}logs${NC} ${GREEN}[--dev][kg gc ui]${NC}

For example if you want to follow the logs for the knowledge graph container in development mode enter the following command:
bash $cli_name ${CYAN}logs${NC} ${GREEN}--dev kg${NC}
"
}


if [[ "$1" == "build" ]]; then
  if [[ "$*" == *" kg"* ]]; then
    build_kg_image
    exit 0
  fi
  if [[ "$*" == *" gc"* ]]; then
    build_graph_connector_image
    exit 0
  fi
  if [[ "$*" == *" ui"* ]]; then
    build_ui_image
    exit 0
  fi
  if [[ "$*" == *" all"* ]]; then
    build_kg_image
    build_graph_connector_image
    build_ui_image
    exit 0
  fi
  show_help
elif [[ "$1" == "start" ]]; then
  if [[ "$2" == "--dev" ]]; then
    start_development "$@"
  else
    start_production
  fi
elif [[ "$1" == "stop" ]]; then
  if [[ "$2" == "--dev" ]]; then
    stop_development
  else
    stop_production
  fi
elif [[ "$1" == "logs" ]]; then
  if [[ "$*" == *" --dev"* ]]; then
    if [[ "$*" == *" kg"* ]]; then
      show_dev_logs fuseki
    elif [[ "$*" == *" gc"* ]]; then
      show_dev_logs graph-connector
    elif [[ "$*" == *" ui"* ]]; then
      show_dev_logs ui
    else
      show_logs_help
    fi
  else
    if [[ "$*" == *" kg"* ]]; then
      show_logs fuseki
    elif [[ "$*" == *" gc"* ]]; then
      show_logs graph-connector
    elif [[ "$*" == *" ui"* ]]; then
      show_logs ui
    else
      show_logs_help
    fi
  fi
else
  show_help
fi

