# AWS EC2 Scheduled Automation

Automating the daily startup and shutdown of Amazon EC2 instances using AWS Lambda, Python (Boto3), and Amazon EventBridge Scheduler.

## 📌 Project Overview
Running cloud instances continuously when they are not needed can significantly increase infrastructure costs. 

This project implements a serverless, automated scheduling system that safely starts two EC2 instances every morning and stops them every evening. This solution eliminates the need for manual operations or a continuously running management server, directly lowering compute costs.

## 🏗️ Architecture

```text
             Amazon EventBridge Scheduler
                         |
             +-----------+-----------+

             |                       |
       8:00 AM EAT               8:00 PM EAT

             |                       |
             v                       v
      AWS Lambda: Starter     AWS Lambda: Stopper

             |                       |
             v                       v
       Amazon EC2 Instances (2)

             |                       |
        Start instances          Stop instances
```

### 🛠️ AWS Services Used

| Service | Purpose |
| :--- | :--- |
| **Amazon EC2** | Hosts the two virtual servers (`cloudops-server-01` & `02`). |
| **AWS Lambda** | Executes the Python automation functions on-demand. |
| **Amazon EventBridge Scheduler** | Triggers the Lambda functions precisely on a daily schedule. |
| **AWS IAM** | Securely controls permissions and roles between AWS services. |
| **Amazon CloudWatch** | Provides centralized execution logs for tracking and debugging. |
| **Boto3 SDK** | The Python SDK used to interact with the underlying AWS EC2 APIs. |

---

## 🚀 Implementation Details

### 1. Amazon EC2 Instances
Two target EC2 instances are managed by this automation framework:
* `cloudops-server-01`
* `cloudops-server-02`

### 2. AWS Lambda Functions
Two isolated Python Lambda functions run the state-change logic:
* **Starter Function (`cloudops-ec2-starter`):** Identifies configured instances that are currently `stopped` and triggers their boot sequence using Boto3.
* **Stopper Function (`cloudops-ec2-stopper`):** Identifies configured instances that are currently `running` and safely initiates a shutdown sequence using Boto3.

*Note: Both functions explicitly check and validate current instance states before attempting execution to prevent unnecessary API calls.*

### 3. Amazon EventBridge Scheduler
Two daily cron schedules are deployed and active:

| Schedule Name | Trigger Time | Time Zone | Target Action |
| :--- | :--- | :--- | :--- |
| `cloudops-ec2-morning-startup` | 8:00 AM | Africa/Addis_Ababa | Invoke `cloudops-ec2-starter` |
| `cloudops-ec2-evening-shutdown` | 8:00 PM | Africa/Addis_Ababa | Invoke `cloudops-ec2-stopper` |

### 4. IAM Permissions & Security Roles
Security profiles are locked down following the **principle of least privilege**:
* **EC2 Automation Lambda Role:** Permits the Lambda functions to run `DescribeInstances`, `StartInstances`, and `StopInstances` API calls *only* on the explicitly designated resource ARNs.
* **EventBridge Execution Role:** A standalone trust role that permits the EventBridge Scheduler service exclusively to invoke the target Lambda functions.

---

## 🧪 Testing and Results
The full end-to-end automation lifecycle was tested and verified in a live AWS sandbox:
- [x] **Manual Verification:** Invoking the shutdown Lambda directly stopped both instances successfully.
- [x] **State Verification:** Invoking the startup Lambda directly brought both instances back online.
- [x] **Schedule Check:** EventBridge schedules were verified as enabled and triggered flawlessly at the exact time boundaries.
- [x] **Result:** Both instances were verified as cleanly stopped at night and active the following morning. The workflow is fully operational.

---

## 🔒 Security & Cost Considerations

### Security Best Practices
* **Zero Hardcoding:** No static AWS access keys, secret keys, or passwords are saved or committed to Git. All access is controlled entirely via IAM execution roles.
* **Network Isolation:** Review and restrict security group rules to only allow required traffic down to the minimum necessary network access.

### Cost Awareness
* Stopping instances drops compute costs (`vCPU/RAM`) to zero during offline hours.
* Keep in mind that provisioned **Amazon EBS storage volumes**, **allocated public IPv4 addresses**, and other baseline static resources will continue to incur standard hourly fees while instances sit in a stopped state.

---

## 💼 Skills Demonstrated
* AWS Cloud Infrastructure Management
* Python Scripting & Cloud Automation
* AWS SDK Integration via Boto3
* Serverless Compute Engine (AWS Lambda)
* Event-Driven Scheduling (Amazon EventBridge)
* AWS IAM Security Profile Management
* Cloud Monitoring, Logging & Troubleshooting
* Cost-Optimization Architecture

---

## 📈 Future Improvements
* [ ] **Alarms:** Add Amazon CloudWatch Alarms for function timeouts or operational state errors.
* [ ] **Notifications:** Route real-time failure alerts to engineers using Amazon SNS.
* [ ] **Testing:** Write local unit tests for the Python automation handlers using `pytest` and `moto`.
* [ ] **Infrastructure as Code (IaC):** Convert manual resource setups into fully repeatable **Terraform** configurations.

---

## 👨‍💻 Author
**Electromechanical Engineering Graduate | AWS Certified Cloud Practitioner**  
*Aspiring CloudOps and Cloud Support Engineer*

## Documentation

- [Architecture](doc/architecture.md) — AWS components and execution flow.
- [Deployment Guide](# AWS EC2 Scheduled Automation

Automating the daily startup and shutdown of Amazon EC2 instances using AWS Lambda, Python (Boto3), and Amazon EventBridge Scheduler.

## 📌 Project Overview
Running cloud instances continuously when they are not needed can significantly increase infrastructure costs. 

This project implements a serverless, automated scheduling system that safely starts two EC2 instances every morning and stops them every evening. This solution eliminates the need for manual operations or a continuously running management server, directly lowering compute costs.

## 🏗️ Architecture

```text
             Amazon EventBridge Scheduler
                         |
             +-----------+-----------+

             |                       |
       8:00 AM EAT               8:00 PM EAT

             |                       |
             v                       v
      AWS Lambda: Starter     AWS Lambda: Stopper

             |                       |
             v                       v
       Amazon EC2 Instances (2)

             |                       |
        Start instances          Stop instances
```

### 🛠️ AWS Services Used

| Service | Purpose |
| :--- | :--- |
| **Amazon EC2** | Hosts the two virtual servers (`cloudops-server-01` & `02`). |
| **AWS Lambda** | Executes the Python automation functions on-demand. |
| **Amazon EventBridge Scheduler** | Triggers the Lambda functions precisely on a daily schedule. |
| **AWS IAM** | Securely controls permissions and roles between AWS services. |
| **Amazon CloudWatch** | Provides centralized execution logs for tracking and debugging. |
| **Boto3 SDK** | The Python SDK used to interact with the underlying AWS EC2 APIs. |

---

## 🚀 Implementation Details

### 1. Amazon EC2 Instances
Two target EC2 instances are managed by this automation framework:
* `cloudops-server-01`
* `cloudops-server-02`

### 2. AWS Lambda Functions
Two isolated Python Lambda functions run the state-change logic:
* **Starter Function (`cloudops-ec2-starter`):** Identifies configured instances that are currently `stopped` and triggers their boot sequence using Boto3.
* **Stopper Function (`cloudops-ec2-stopper`):** Identifies configured instances that are currently `running` and safely initiates a shutdown sequence using Boto3.

*Note: Both functions explicitly check and validate current instance states before attempting execution to prevent unnecessary API calls.*

### 3. Amazon EventBridge Scheduler
Two daily cron schedules are deployed and active:

| Schedule Name | Trigger Time | Time Zone | Target Action |
| :--- | :--- | :--- | :--- |
| `cloudops-ec2-morning-startup` | 8:00 AM | Africa/Addis_Ababa | Invoke `cloudops-ec2-starter` |
| `cloudops-ec2-evening-shutdown` | 8:00 PM | Africa/Addis_Ababa | Invoke `cloudops-ec2-stopper` |

### 4. IAM Permissions & Security Roles
Security profiles are locked down following the **principle of least privilege**:
* **EC2 Automation Lambda Role:** Permits the Lambda functions to run `DescribeInstances`, `StartInstances`, and `StopInstances` API calls *only* on the explicitly designated resource ARNs.
* **EventBridge Execution Role:** A standalone trust role that permits the EventBridge Scheduler service exclusively to invoke the target Lambda functions.

---

## 🧪 Testing and Results
The full end-to-end automation lifecycle was tested and verified in a live AWS sandbox:
- [x] **Manual Verification:** Invoking the shutdown Lambda directly stopped both instances successfully.
- [x] **State Verification:** Invoking the startup Lambda directly brought both instances back online.
- [x] **Schedule Check:** EventBridge schedules were verified as enabled and triggered flawlessly at the exact time boundaries.
- [x] **Result:** Both instances were verified as cleanly stopped at night and active the following morning. The workflow is fully operational.

---

## 🔒 Security & Cost Considerations

### Security Best Practices
* **Zero Hardcoding:** No static AWS access keys, secret keys, or passwords are saved or committed to Git. All access is controlled entirely via IAM execution roles.
* **Network Isolation:** Review and restrict security group rules to only allow required traffic down to the minimum necessary network access.

### Cost Awareness
* Stopping instances drops compute costs (`vCPU/RAM`) to zero during offline hours.
* Keep in mind that provisioned **Amazon EBS storage volumes**, **allocated public IPv4 addresses**, and other baseline static resources will continue to incur standard hourly fees while instances sit in a stopped state.

---

## 💼 Skills Demonstrated
* AWS Cloud Infrastructure Management
* Python Scripting & Cloud Automation
* AWS SDK Integration via Boto3
* Serverless Compute Engine (AWS Lambda)
* Event-Driven Scheduling (Amazon EventBridge)
* AWS IAM Security Profile Management
* Cloud Monitoring, Logging & Troubleshooting
* Cost-Optimization Architecture

---

## 📈 Future Improvements
* [ ] **Alarms:** Add Amazon CloudWatch Alarms for function timeouts or operational state errors.
* [ ] **Notifications:** Route real-time failure alerts to engineers using Amazon SNS.
* [ ] **Testing:** Write local unit tests for the Python automation handlers using `pytest` and `moto`.
* [ ] **Infrastructure as Code (IaC):** Convert manual resource setups into fully repeatable **Terraform** configurations.

---

## 👨‍💻 Author
**Electromechanical Engineering Graduate | AWS Certified Cloud Practitioner**  
*Aspiring CloudOps and Cloud Support Engineer*

## Documentation

- [Architecture](doc/architecture.md) — AWS components and execution flow.
- [Deployment Guide](docs/deployment.md) — How to deploy the project.
- [EC2 Startup Function](lambda/ec2_starter.py) — Python implementation.
- [EC2 Shutdown Function](lambda/ec2_stopper.py) — Python implementation.)
