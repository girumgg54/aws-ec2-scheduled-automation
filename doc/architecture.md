# AWS EC2 Automation — Architecture

## 1. Overview

This project automates the daily startup and shutdown of two
Amazon EC2 instances using AWS Lambda and Amazon EventBridge Scheduler.

The solution reduces the need for manual instance management and
can reduce compute costs when instances are not needed.

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
              3. AWS Components
Amazon EC2
Two EC2 instances are managed by the automation:
- cloudops-server-01
- cloudops-server-02
AWS Lambda
Two Python functions perform the instance-state operations.
Startup function
- Receives an invocation from EventBridge Scheduler.
- Checks the configured instances.
- Starts instances that are stopped.
Shutdown function
- Receives an invocation from EventBridge Scheduler.
- Checks the configured instances.
- Stops instances that are running.
Both functions use Boto3 to call the EC2 API.
Amazon EventBridge Scheduler
Two enabled schedules trigger the Lambda functions daily.
Schedule	Time	Time zone	Target
Morning startup	08:00	Africa/Addis_Ababa	cloudops-ec2-starter
Evening shutdown	20:00	Africa/Addis_Ababa	cloudops-ec2-stopper


AWS IAM
Two permission boundaries are important to the design:
1. The Lambda execution role grants the functions the EC2 permissions
   needed to inspect and change the state of the designated instances.
2. The EventBridge Scheduler execution role allows the scheduler
   to invoke the designated Lambda functions.
These permissions should be restricted to the required resources.
4. Execution Flow
Morning startup
1. EventBridge Scheduler reaches the configured morning time.
2. Scheduler invokes cloudops-ec2-starter.
3. Lambda checks the configured EC2 instances.
4. Instances in the stopped state are started.
5. The function logs and returns the result.
Evening shutdown
1. EventBridge Scheduler reaches the configured evening time.
2. Scheduler invokes cloudops-ec2-stopper.
3. Lambda checks the configured EC2 instances.
4. Instances in the running state are stopped.
5. The function logs and returns the result.
5. Monitoring and Troubleshooting
CloudWatch Logs can be used to inspect Lambda execution output.
If an invocation fails, check:
- The Lambda execution role and EC2 permissions.
- The EventBridge Scheduler execution role.
- The configured Lambda target.
- The schedule's enabled status and time zone.
- The instance IDs and AWS Region.
- Lambda execution logs and any reported errors.
6. Cost Considerations
Stopping an EC2 instance generally stops its instance compute charges,
but other resources may continue to incur charges.
Examples include EBS volumes and public IPv4 addresses.
Review AWS Billing and Credits regularly.
7. Verified Results
The project was tested in AWS.
- Both EC2 instances were stopped by the shutdown automation.
- Both instances were started by the startup automation.
- Both daily schedules were enabled.
- The instances were observed stopped at night and running again
  after the morning schedule.
8. Future Improvements
- Add CloudWatch alarms.
- Send failure notifications using Amazon SNS.
- Introduce automated Python tests with pytest.
- Manage the infrastructure using Terraform.
- Add deployment instructions and configuration validation.
