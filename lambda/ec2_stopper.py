import json
import os

import boto3

REGION = os.environ.get("AWS_REGION", "af-south-1")

ec2 = boto3.client("ec2", region_name=REGION)

INSTANCE_IDS = [
    "i-0b44dac3aabb9f73f",
    "i-0fc64c4e422be6e2a",
]


def lambda_handler(event, context):
    """Stop configured EC2 instances that are currently running."""

    response = ec2.describe_instances(
        InstanceIds=INSTANCE_IDS,
        Filters=[
            {
                "Name": "instance-state-name",
                "Values": ["running"],
            }
        ],
    )

    running_instances = [
        instance["InstanceId"]
        for reservation in response["Reservations"]
        for instance in reservation["Instances"]
    ]

    if not running_instances:
        result = {
            "message": "No running instances found.",
            "stopped_instances": [],
        }
    else:
        ec2.stop_instances(InstanceIds=running_instances)

        result = {
            "message": "Shutdown initiated.",
            "stopped_instances": running_instances,
        }

    print(json.dumps(result))
    return result
