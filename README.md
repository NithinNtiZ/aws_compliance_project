# Project Overview

This project involves two Python scripts deployed for AWS compliance and monitoring purposes. Below is a brief description of each script along with its deployment details.

## 1. `all_autotag.py`

### Description
- **File Path**: GIT repo:aws_compliance_project\aws_compliance_autotag\all_autotag.py
- **Functionality**: Tags all the instances with required tags for AWS compliance.
- **Deployment**: Deployed as a Lambda function.
- **Trigger**: Triggered by CloudWatch event.

## 2. `all_instances.py`

### Description
- **File Path**: GIT repo:aws_compliance_project\aws_grafana_lease_expire_monitoring\script_aws_data\all_instances.py
- **Functionality**: Collects all instance data and pushes it to a MySQL database.
- **Deployment**: Docker compose is used to deploy the script and the database.
- **Integration**: MySQL database is used as a datasource for Grafana.
- **Monitoring**: Dashboard created in Grafana using the MySQL data for monitoring purposes.

## 3. Deployment Docker Compose File

- **File Path**: GIT repo:aws_compliance_project\aws_grafana_lease_expire_monitoring\dep_docker_compose\docker-compose.yml
- Ensure that the correct data is properly passed to the .env file

This markdown file provides an overview of the scripts, their functionalities, and deployment details within the AWS compliance project.
