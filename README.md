# AWS EC2 Scheduled Automation

Automating the daily startup and shutdown of Amazon EC2 instances using
AWS Lambda, Python (Boto3), and Amazon EventBridge Scheduler.

## Project Overview

Running cloud instances continuously when they are not needed can
increase infrastructure costs.

This project implements a scheduled automation system that starts
two EC2 instances every morning and stops them every evening.

The solution uses serverless AWS services to manage instance states
automatically without requiring a continuously running management server.

## Architecture

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
