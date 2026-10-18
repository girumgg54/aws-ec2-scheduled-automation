# AWS EC2 Automation — Architecture

## 1. Overview
This project automates the daily startup and shutdown of two Amazon EC2 instances using AWS Lambda and Amazon EventBridge Scheduler.

The solution reduces the need for manual instance management and can reduce compute costs when instances are not needed.

## 2. Architecture Diagram

```text
                 Amazon EventBridge Scheduler
                              |
                 +------------+------------+

                 |                         |
          Morning Schedule           Evening Schedule
             08:00 EAT                   20:00 EAT

                 |                         |
                 v                         v
        cloudops-ec2-starter      cloudops-ec2-stopper

                 |                         |
                 +------------+------------+
                              |
                              v
                     Amazon EC2 API
                              |
                    +---------+---------+

                    |                   |
                    v                   v
              EC2 Instance 1      EC2 Instance 2
```

## 3. AWS Components

### 🖥️ Amazon EC2
Two EC2 instances are managed by the automation:
* `cloudops-server-01`
* `cloudops-server-02`

### ⚡ AWS Lambda
Two Python functions perform the instance-state operations using the Boto3 SDK:
* **Startup function (`cloudops-ec2-starter`):** Receives an invocation from EventBridge Scheduler, checks the configured instances, and starts them if they are stopped.
* **Shutdown function (`cloudops-ec2-stopper`):** Receives an invocation from EventBridge Scheduler, checks the configured instances, and stops them if they are running.

### ⏰ Amazon EventBridge Scheduler
Two enabled schedules trigger the Lambda functions daily:

| Schedule | Time | Time zone | Target |
| :--- | :--- | :--- | :--- |
| **Morning startup** | 08:00 | Africa/Addis_Ababa | `cloudops-ec2-starter` |
| **Evening shutdown** | 20:00 | Africa/Addis_Ababa | `cloudops-ec2-stopper` |

### 🔐 AWS IAM
Two permission boundaries are critical to the design:
1. **Lambda Execution Role:** Grants the functions the exact EC2 permissions needed to inspect and change the state of the designated instances.
2. **EventBridge Scheduler Execution Role:** Allows the scheduler to securely invoke the designated Lambda functions.

*Note: These permissions should always follow the principle of least privilege and be restricted to the required resources.*

## 4. Execution Flow

### 🌅 Morning Startup
1. EventBridge Scheduler reaches the configured morning time (08:00 EAT).
2. Scheduler invokes `cloudops-ec2-starter`.
3. Lambda checks the status of the configured EC2 instances.
4. Instances found in the `stopped` state are started.
5. The function logs the execution metadata and returns the result.

### 🌌 Evening Shutdown
1. EventBridge Scheduler reaches the configured evening time (20:00 EAT).
2. Scheduler invokes `cloudops-ec2-stopper`.
3. Lambda checks the status of the configured EC2 instances.
4. Instances found in the `running` state are stopped.
5. The function logs the execution metadata and returns the result.

## 5. Monitoring and Troubleshooting
AWS CloudWatch Logs can be used to inspect Lambda execution output. If an invocation fails, verify the following details:
* The Lambda execution role and its specific EC2 permissions.
* The EventBridge Scheduler execution role trust relationship.
* The configured Lambda target ARN.
* The schedule's enabled status and regional time zone configurations.
* The explicit instance IDs and target AWS Region.

## 6. Cost Considerations
Stopping an EC2 instance stops its instance compute charges, but associated resources may continue to incur charges. Examples include:
* Provisioned Amazon EBS volumes.
* Allocated public IPv4 addresses.

*Tip: Review your AWS Billing and Cost Explorer regularly to track overall project savings.*

## 7. Verified Results
The project architecture was fully deployed and verified in a live AWS environment:
- [x] Both EC2 instances were successfully stopped by the shutdown automation.
- [x] Both EC2 instances were successfully started by the startup automation.
- [x] Both daily schedules were verified as enabled and active.
- [x] Target instances were confirmed stopped at night and running during day hours.

## 8. Future Improvements
* Add Amazon CloudWatch Alarms for state-change failures.
* Send real-time failure alerts using Amazon SNS (Email/SMS).
* Introduce automated unit tests for Python using `pytest`.
* Convert the infrastructure into reusable Infrastructure as Code (IaC) using **Terraform**.
* Add localized deployment instructions and input configuration validation.
