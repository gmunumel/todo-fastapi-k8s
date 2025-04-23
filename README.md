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

    eksctl create cluster -f cluster-config.yml

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

## Using ELK-B

Sources:

- https://github.com/elkninja/elastic-stack-docker-part-one/tree/main
- https://github.com/elastic/elasticsearch/blob/8.17/docs/reference/setup/install/docker/docker-compose.yml
- https://github.com/gnokoheat/elk-with-filebeat-by-docker-compose/tree/master
- https://discuss.elastic.co/t/invalid-protocol-when-filebeat-send-to-logstash/316681/13?u=gabrielmunumel

Run _ELK_ as docker container using [docker-compose.yml](elk-b/docker-compose.yml).

You can run it as (`-d` is to run on background):

    docker compose -f elk-b/docker-compose.yml up -d

To remove the docker compose (remove volumes too with `-v`):

    docker compose -f elk-b/docker-compose.yml down -v

In case of any error with `Filebeat`, `Logstash`, `ElasticSearch` or `Kibana`:

    docker-compose -f elk-b/docker-compose.yml restart filebeat01
    docker-compose -f elk-b/docker-compose.yml restart logstash01
    docker-compose -f elk-b/docker-compose.yml restart es01
    docker-compose -f elk-b/docker-compose.yml restart kibana

Logstash configuration is in [logstash.conf](elk-b/logstash.conf).

Copy the `es01` certificate:

    docker cp es01:/usr/share/elasticsearch/config/certs/ca/ca.crt /tmp/.

If everything is running fine you would see an index `todo-fastapi-k8s-logs` when run:

    curl --cacert /tmp/ca.crt -u elastic:changeme -X GET "https://localhost:9200/_cat/indices?v"

    or

    curl -X GET "http://localhost:9200/_cat/indices?v"

    docker exec -it filebeat01 curl logstash01:5044

In case Kibana ask for a "Enrollment token", execute this and try again:

    docker exec -it elasticsearch bin/elasticsearch-reset-password -u elastic

### Access Kibana

1.  Open Kibana in your browser: http://localhost:5601.
2.  User: `elastic` and password: it's in `.env` file.
3.  Configure an index pattern for `todo-fastapi-k8s-logs` in Kibana to start visualizing logs.
    - In the Kibana sidebar, click on "Stack Management".
    - Under the "Kibana" section, click on "Data Views".
    - Click on "Create a data view"
4.  Create a data view

    - Define the following fields:

            Name: todo-fastapi-k8s-logs
            Index pattern: filebeat-*
            Timestand field: @timestamp

    - Click on "Save data view to Kibana".

5.  Then go to Discover and you should see the logs coming in.

#### Activate Stack Monitoring

1. Go to "Stack Monitoring" in "Management" section on the sidebar.
2. Click on "Yes" and "Ok".
