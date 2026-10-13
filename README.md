# FastAPI on Kubernetes (minikube)

A small FastAPI app packaged in Docker and run on a local Kubernetes cluster (minikube with the Docker driver). It serves on port 5000 inside the container and is exposed through a NodePort Service.

## Project layout

- `src/main.py`: the FastAPI app
- `Dockerfile`: builds the image (uvicorn serving `src.main:app` on port 5000)
- `requirements.txt`: Python dependencies
- `fastapi-app.yaml`: Kubernetes Deployment (2 replicas) and NodePort Service

## Prerequisites

Docker, minikube and kubectl installed, with Docker running.

## 1. Start the cluster

Starts a local single-node Kubernetes cluster inside a Docker container. `kubectl get nodes` should show the node as Ready.

```
minikube start --driver=docker
kubectl get nodes
```

## 2. Build the image inside minikube

Run this in the folder with the Dockerfile. The image must be built into minikube itself, because the Deployment uses `imagePullPolicy: Never` and will not pull from a registry. The second command confirms the image is there.

```
minikube image build -t fastapi-app:1.0 .
minikube image ls | grep fastapi
```

## 3. Deploy

Creates the Deployment (the pods) and the Service (the network entry point) from the YAML file. Pods should reach Running status.

```
kubectl apply -f fastapi-app.yaml
kubectl get pods
```

## 4. Get the URL and test

Prints the address of the Service and opens a tunnel if needed. Keep that terminal open while testing, and use a second terminal for curl.

```
minikube service fastapi-app --url
curl <url>
```

## After a code change

Rebuild the image, then restart the Deployment so it creates new pods from the new image. The old pods are removed automatically.

```
minikube image build -t fastapi-app:1.0 .
kubectl rollout restart deployment fastapi-app
kubectl get pods
```

## Debugging

Use these when a pod is not Running. `logs` shows the app's error output, and `describe` shows Kubernetes events such as image pull problems.

```
kubectl get pods
kubectl logs <pod-name>
kubectl describe pod <pod-name>
```

Common statuses:

- `ErrImageNeverPull`: the image is not inside minikube, rebuild it with step 2
- `CrashLoopBackOff` or `Error`: the container crashes on start, check the logs

## Clean up

Removes the Deployment and Service, then stops the cluster. Use `minikube delete` only to wipe the whole cluster, which also removes the images inside it.

```
kubectl delete -f fastapi-app.yaml
minikube stop
```