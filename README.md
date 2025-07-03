In this project, we will build a soccer leagues standings API. 
The project consists a FastAPI backend serving a GET-only API, a Flask frontend serving a landing page (documentation UI) and a MongoDB database for storing league standings. 
All components will be containerized with Docker and deployed to Kubernetes using Deployments, Services ,Ingress and secret. 

***Start:***

1) Open a new GitHub repo, pull the repo into the cloud shell and config the GitHub user for a future Push requests.

2) Enable "Kubernetes Engine API" (for GCP).

3) Set up your default region and zone:
```bash
gcloud config set compute/region your_region
gcloud config set compute/zone your_zone
```
4) Set up a Git ignore file.

5) Apply a Terraform script that will set up a VPC Network, Subnet, GKE Cluster, NGINX Ingress Controller and Kubernetes Apps via Helm (Jenkins, ArgoCD, Mongo).

6) Set up a script that will automate the push of the future new files into this repository.
```bash
#!/bin/bash

USERNAME="your_user"
TOKEN="${GITHUB_PAT}"

git remote set-url origin https://$USERNAME:$TOKEN@github.com/$USERNAME/your_repo.git

git add .
git commit -m "Initial commit"
git push origin main
```
```bash
export GITHUB_PAT=your_PAT
```
Make the script executable and run it:
```bash
chmod +x push.sh
./push.sh
```

**DB:**
Get into the Mongo container inside the Mongo app pod.
Create the DB that you want to use, create one collection for every league and create one documentation for every team the team's stats.

**Backend:**
The backend will use FastAPI to expose an HTTP GET endpoint /api/standings/{league_name} that returns the standings for the requested league. The data will be fetched from a MongoDB collection matching to the league name.

Codes: Create a single FastAPI code to define the single GET endpoint and to define the connection to the Mongo pod.

**Frontend:**
The frontend will use Flask to serve a static documentation page for the API.
This will be the landing page that users can visit to learn about the API, see available endpoints, and understand how to use it.

Codes: Create a Flask app code that defines the root path "/", which renders an HTML template (create the HTML template code too).

**Docker:**
Create Docker files for the backend app and the frontend app, create an images and push into DockerHub.

**Kubernetes:**

