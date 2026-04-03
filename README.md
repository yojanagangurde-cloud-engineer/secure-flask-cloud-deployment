# Secure Flask Cloud Deployment (AWS + Docker + RDS)

## Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Networking](#-networking)
- [Security Features](#-security-features)
- [Storage](#-storage)
- [Monitoring & Logging](#-monitoring--logging)
- [Scalability](#-scalability)
- [Deployment Steps](#-deployment-steps)
- [Screenshots](#-screenshots)
- [What This Project Demonstrates](#-what-this-project-demonstrates)
- [Author](#-author)

## Overview
This project demonstrates a production-ready Flask application deployed on AWS using modern cloud, security, and DevOps best practices.

The application is containerized using Docker, hosted on EC2, and connected to a PostgreSQL database running on Amazon RDS in a private network.

It includes:

- Dockerized Flask application running on EC2
- PostgreSQL database hosted on Amazon RDS
- Secure VPC architecture with public and private subnets across multiple AZs
- IAM-based access control (no hardcoded credentials)
- Monitoring with CloudWatch and logging with CloudTrail
- Auto Scaling Group for high availability
- S3 used for storage and logs


## Architecture
![Architecture](architecture/aws-architecture.png)

## Tech Stack

- Python (Flask)
- Docker
- AWS EC2
- AWS RDS (PostgreSQL)
- AWS VPC (Public & Private Subnets)
- AWS IAM (Roles & Permissions)
- AWS S3
- AWS CloudWatch
- AWS CloudTrail
- AWS Auto Scaling

## Networking

- Custom VPC created
- **Public Subnet**:
  - Hosts EC2 instance (Flask app)
  - Connected to Internet Gateway
- **Private Subnets (2 AZs)**:
  - Host RDS database
  - No public internet access
- Route tables configured for secure traffic flow

## Security Features

- RDS deployed in private subnets (not publicly accessible)
### EC2 Security Group:
- SSH (22) → Only from my IP
- HTTP (80) → Public
- HTTPS (443) → Public
- Custom Port (5001) → Public (Flask app)
    - PostgreSQL (5432) — only from EC2 security group
- IAM Role attached to EC2 (no hardcoded credentials)
- Secrets stored using environment variables:
  - `DATABASE_URL`
  - `SECRET_KEY`
- CloudTrail enabled for auditing AWS activity

## Storage

- Amazon S3 used for storing logs and artifacts
- CloudTrail logs stored securely in S3

## Monitoring & Logging

- CloudWatch configured for:
  - EC2 CPU utilization
  - RDS CPU utilization
- Alerts triggered when thresholds exceed limits
- CloudTrail logs all API activity for auditing

## Scalability

- Auto Scaling Group configured:
  - Uses launch template
  - Automatically replaces unhealthy instances
  - Ensures high availability

## Deployment Steps

1. Clone Repository

git clone https://github.com/yojanagangurde-cloud-engineer/secure-flask-cloud-deployment.git

2. Set Environment Variables

export DATABASE_URL=postgresql://postgres:strongpassword@flask-postgres-db.c03m026we7u0.us-east-1.rds.amazonaws.com:5432/market_db
SECRET_KEY=supersecretkey123

3. Build Docker Image

docker build -t flask-app .

4. Run Docker Container
docker run -d -p 5001:5001 \
-e DATABASE_URL=$DATABASE_URL \
-e SECRET_KEY=$SECRET_KEY \
--name flask-container flask-app

## Screenshots

### Application Pages

#### Home Page
![Home Page](screenshots/Flask-app-working/App-Home-Page.png)

#### Login Page
![Login Page](screenshots/Flask-app-working/App-Login-Page.png)

#### Registration Page
![Registration Page](screenshots/Flask-app-working/App-Registration-Page.png)

#### Signup Page
![Signup Page](screenshots/Flask-app-working/App-SignUp-Page.png)

#### Successful Login
![Successful Login](screenshots/Flask-app-working/App-Successfullogin-Page.png)

#### Cart Page
![Cart Page](screenshots/Flask-app-working/App-Cart-Page.png)

#### Checkout Page
![Checkout Page](screenshots/Flask-app-working/App-Checkout-Page.png)

#### Order Placed
![Order Placed](screenshots/Flask-app-working/App-Order-Placed.png)


### AWS Infrastructure

#### EC2 Instance
![EC2](screenshots/EC2.png)

#### EC2 Security Group (Inbound Rules)
![EC2 SG Inbound](screenshots/EC2-SG-inbound.png)

#### EC2 Security Group (Outbound Rules)
![EC2 SG Outbound](screenshots/EC2-SG-outbound.png)

#### IAM Role
![IAM Role](screenshots/iam-role.png)

#### VPC Configuration
![VPC](screenshots/vpc.png)


### RDS (PostgreSQL)

#### RDS Overview
![RDS Overview](screenshots/RDS-Overview.png)

#### RDS Configuration
![RDS Config](screenshots/RDS-Configurations.png)

#### RDS Connectivity
![RDS Connectivity](screenshots/RDS-connectivity.png)

#### RDS Security Group
![RDS SG](screenshots/RDS-SG.png)


### Monitoring & Scaling

#### CloudWatch Alarms
![CloudWatch](screenshots/cloudwatch-alarms.png)

#### CloudTrail Logs
![CloudTrail](screenshots/cloudtrail.png)

#### Auto Scaling Group
![Auto Scaling](screenshots/autoscaling.png)

### Storage

#### S3 Bucket
![S3](screenshots/s3.png)


## What This Project Demonstrates
- Secure cloud architecture using AWS
- Separation of public and private resources
- Database isolation in private subnet
- Docker containerization of Flask app
- IAM role-based access control
- Monitoring and logging setup
- Auto Scaling and high availability
- Production-ready deployment workflow


Author

Yojana Gangurde
GitHub: https://github.com/yojanagangurde-cloud-engineer/secure-flask-cloud-deployment

