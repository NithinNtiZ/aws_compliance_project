`before deploying any k8 container, imagepull secret must be deployed to the desired name space`

kubectl create secret docker-registry myregistrykey --docker-server=supportlab.azurecr.io --docker-username=supportlab --docker-password= --namespace=grafana_aws