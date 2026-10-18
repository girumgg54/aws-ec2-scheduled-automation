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
    """Start configured EC2 instances that are currently stopped."""

    response = ec2.describe_instances(
        InstanceIds=INSTANCE_IDS,
        Filters=[
            {
                "Name": "instance-state-name",
                "Values": ["stopped"],
            }
        ],
    )

    stopped_instances = [
        instance["InstanceId"]
        for reservation in response["Reservations"]
        for instance in reservation["Instances"]
    ]

    if not stopped_instances:
        result = {
            "message": "No stopped instances found.",
            "started_instances": [],
        }
    else:
        ec2.start_instances(InstanceIds=stopped_instances)

        result = {
            "message": "Startup initiated.",
            "started_instances": stopped_instances,
        }

    print(json.dumps(result))
    return result
