# Deployment Guide

This guide describes how to deploy the scheduled EC2 startup and
shutdown automation in an AWS account.

## 1. Prerequisites

Before starting, you need:

- An AWS account.
- Access to the AWS Management Console.
- Permission to create and configure EC2, Lambda, IAM, and
  EventBridge Scheduler resources.
- Basic knowledge of Python and AWS IAM.

## 2. Choose the AWS Region

This project was implemented in:

`af-south-1` — Africa (Cape Town)

Use the same region for the EC2 instances and Lambda functions.

## 3. Create EC2 Instances

Create two EC2 instances and give them recognizable names:

- `cloudops-server-01`
- `cloudops-server-02`

Record their instance IDs for Lambda configuration.

Choose instance types and storage appropriate for your workload.

## 4. Configure IAM Permissions

Create an IAM execution role for the Lambda functions.

The role must allow the functions to:

- Describe the configured EC2 instances.
- Start the designated EC2 instances.
- Stop the designated EC2 instances.

Restrict start and stop permissions to the intended instances.

Configure the role's trust policy to allow AWS Lambda to assume it.

Create a separate IAM role for EventBridge Scheduler. Its trust
policy must allow `scheduler.amazonaws.com` to assume the role.

Allow that role to invoke only the two Lambda functions.

## 5. Create the Lambda Functions

Create two Lambda functions using a supported Python runtime.

### Startup function

Function name:

`cloudops-ec2-starter`

Use the code in:

`lambda/ec2_starter.py`

### Shutdown function

Function name:

`cloudops-ec2-stopper`

Use the code in:

`lambda/ec2_stopper.py`

Configure both functions to use the appropriate IAM execution role.

### Configure the instance IDs

In each Python file, replace the placeholder instance IDs with
the IDs of your EC2 instances.

Example:

```python
INSTANCE_IDS = [
    "i-0123456789abcdef0",
    "i-0123456789abcdef1",
]
```

The IDs above are examples only. Use the actual IDs from your account.

Deploy the code and test each function individually before scheduling it.

## 6. Create EventBridge Schedules

Create two schedules in Amazon EventBridge Scheduler.

### Morning startup

- Name: `cloudops-ec2-morning-startup`
- Target: `cloudops-ec2-starter`
- Schedule: Daily at 08:00
- Time zone: `Africa/Addis_Ababa`
- Flexible time window: Off
- Status: Enabled

### Evening shutdown

- Name: `cloudops-ec2-evening-shutdown`
- Target: `cloudops-ec2-stopper`
- Schedule: Daily at 20:00
- Time zone: `Africa/Addis_Ababa`
- Flexible time window: Off
- Status: Enabled

Use the EventBridge execution role configured in Step 4.

## 7. Test the Automation

Before relying on the schedules:

1. Test the startup function with the instances stopped.
2. Confirm that the instances enter the running state.
3. Test the shutdown function with the instances running.
4. Confirm that the instances enter the stopped state.
5. Verify that both schedules are enabled.
6. Inspect Lambda logs in Amazon CloudWatch.
7. Confirm that the schedule targets and time zones are correct.

Allow time for EC2 state transitions to complete.

## 8. Security Considerations

- Never commit AWS credentials or private keys.
- Use least-privilege IAM permissions.
- Keep instance IDs and resource ARNs consistent with your deployment.
- Review security group rules.
- Monitor Lambda execution logs.

## 9. Cost Considerations

Stopping instances reduces their normal compute charges while stopped,
but other resources may continue to incur costs.

Review EBS volumes, public IPv4 addresses, and other associated resources.

Monitor AWS Billing and Credits to track your spending.

## 10. Cleanup

When the project is no longer needed:

1. Disable or delete both EventBridge schedules.
2. Delete the Lambda functions if they are no longer required.
3. Terminate EC2 instances if you no longer need them.
4. Review and remove unused EBS volumes and other billable resources.
5. Remove IAM roles and policies that are no longer needed.

Check dependencies before deleting resources.
