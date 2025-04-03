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

## Deploy to Kubernetes in AWS

    eksctl create cluster --name todo-cluster --region eu-central-1 --nodes 2

## Create a Docker image

### Authenticate Docker with ECR (Optional)

    aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 177539010329.dkr.ecr.eu-central-1.amazonaws.com

### Create an ECR repository

    aws ecr create-repository --repository-name gminc/todo-fastapi-k8s

### Tag and push your Docker image

    docker tag todo-fastapi-k8s:latest 177539010329.dkr.ecr.eu-central-1.amazonaws.com/gminc/todo-fastapi-k8s:latest
    docker push 177539010329.dkr.ecr.eu-central-1.amazonaws.com/gminc/todo-fastapi-k8s:latest

## Using Helm Chart

[Helm Chart](https://helm.sh/) easier deployment of Kubernetes clusters.

### Create a Helm Chart

    helm create todo-fastapi-k8s

This will create a folder: `todo-fastapi-k8s`.

[Chart.yaml](todo-fastapi-k8s/Chart.yaml): update medatada associated to your app. It's already updated.
[values.yaml](todo-fastapi-k8s/values.yaml): define defatult values for your deployment. It's already updated.
[deployment.yaml](todo-fastapi-k8s/templates/deployment.yaml): deployment template details. It's already updated.
[service.yaml](todo-fastapi-k8s/templates/service.yaml): servuce template details. It's already updated.

### Deploy the Helm Chart

Package the Helm chart:

    helm package todo-fastapi-k8s

Deploy the chart to your Kubernetes cluster:

    helm install todo-fastapi-k8s ./todo-fastapi-k8s

Verify the deployment:

    kubectl get pods
    kubectl get service

### Update the Deployment

If you make changes to the chart, upgrade the deployment:

    helm upgrade todo-fastapi-k8s ./todo-fastapi-k8s

### Uninstall the Deployment

    helm uninstall todo-fastapi-k8s

## Delete Resources

### Delete All Kubernetes Resources

    kubectl delete all --all

### Delete Namespaces (if applicable)

    kubectl delete namespace <namespace>

### Delete the EKS Cluster

    eksctl delete cluster --name todo-cluster

## Create Kubernetes Deployment and Service Manually

In [deployment.yaml](deployment.yaml) is a Kubernetes manifests for the FastApi app.

In [service.yaml](service.yaml) is the service.

## Apply Kubernetes Manifests

### Apply the deployment and service

    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml

### Verify the pods are running

    kubectl get pods

### Get the external IP of the LoadBalancer

    kubectl get service todo-fastapi-k8s-service

Now you can access your app `http://<EXTERNAL-IP>`.

## Monitor and Scale

### Use `kubectl` to monitor your application

    kubectl get pods
    kubectl logs <name>
    kubectl logs todo-fastapi-k8s-86784469ff-qvk6b
    kubectl logs todo-fastapi-k8s-86784469ff-wn8sk

### Scale your deployment

    kubectl scale deployment todo-fastapi-k8s --replicas=3
