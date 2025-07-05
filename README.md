In this project, you will enable HTTPS for a Kubernetes application deployed on GKE using a free DuckDNS subdomain and an automated Let’s Encrypt certificate via cert-manager.

The project consists of a Dynamic DNS configuration (DuckDNS), a TLS certificate manager (cert-manager), and a secured Ingress for routing HTTPS traffic to your backend and frontend services.

All components will be deployed to Kubernetes using standard manifests: Ingress, Secret, Certificate, ClusterIssuer, and Services.

***Start:***

1) Open a new GitHub repo, pull the repo into the cloud shell and config the GitHub user for a future Push requests.

2) Create a DuckDNS account and a subdomain:  
Go to 'https://www.duckdns.org/', sign in with GitHub, and register a new subdomain (e.g. 'myapi.duckdns.org').

3) Copy the external IP of your NGINX Ingress Controller and set it as the IP address for the DuckDNS subdomain using the DuckDNS dashboard.

4) Confirm DNS is configured correctly:
```bash
nslookup myapi.duckdns.org
dig +short myapi.duckdns.org
```
Both commands should return the external IP of your NGINX Ingress Controller.

5) Install cert-manager into the cluster:
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.2/cert-manager.yaml
```

6) Wait for all cert-manager pods to be in 'Running' status:
```bash
kubectl get pods -n cert-manager
```
You should see the following pods:
- cert-manager
- cert-manager-webhook
- cert-manager-cainjector

**ClusterIssuer:**  
Create a ClusterIssuer to register with Let’s Encrypt and manage certificate generation.

File: 'clusterissuer.yaml'
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your_email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod-account-key
    solvers:
    - http01:
        ingress:
          ingressClassName: nginx
```
Apply the ClusterIssuer:
```bash
kubectl apply -f clusterissuer.yaml
```

**Certificate:**  
Create a Certificate resource to request an HTTPS certificate for your DuckDNS domain.

File: 'certificate.yaml'
```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: myapi-duckdns-cert
  namespace: default
spec:
  secretName: myapi-tls
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
  - myapi.duckdns.org
```
Apply the Certificate:
```bash
kubectl apply -f certificate.yaml
```

Check that the certificate was successfully issued:
```bash
kubectl describe certificate myapi-duckdns-cert
kubectl get secret myapi-tls
```

**Ingress:**  
Update the Ingress to use the TLS certificate for HTTPS termination.

File: 'ingress.yaml'
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: football-ingress
  namespace: default
  annotations:
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  ingressClassName: nginx
  rules:
  - host: myapi.duckdns.org
    http:
      paths:
      - path: /api/standings
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 8000
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 5000
  tls:
  - hosts:
    - myapi.duckdns.org
    secretName: myapi-tls
```
Apply the Ingress:
```bash
kubectl apply -f ingress.yaml
```

**Validation:**  
Test that HTTPS is working:
```bash
curl -I https://myapi.duckdns.org
curl -I http://myapi.duckdns.org
```
You should receive a `200 OK` for HTTPS and a `301/302` redirect from HTTP to HTTPS.


