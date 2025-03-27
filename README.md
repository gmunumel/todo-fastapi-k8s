![Test Status](https://github.com/gmunumel/todo-fastapi-k8s/actions/workflows/python-tests.yml/badge.svg)

# todo-fastapi-k8s

This is a simple Todo list using FastAPI and Kubernetes

## Using virtual environment

Create a virtual environment:

    python -m venv .venv

Activate the virtual environment:

In windows:

    . ./.venv/Scripts/activate

In linux:

    source .venv/bin/activate

## Install the libraries

    pip install .

or

    pip install .[test]

## Run the application

    uvicorn src.main:app --reload

## Run the tests

    pytest -v

## Run Docker container

    docker build -t todo-fastapi-k8s . && docker run -p 8000:8000 --rm --name "todo-fastapi-k8s" todo-fastapi-k8s
