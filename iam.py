#!/usr/bin/env python3
import boto3
import botocore


PROFILE_NAME = "LabInstanceProfile"
REGION = "us-west-2"

ec2 = boto3.client("ec2", region_name=REGION)

# 2. Ask AWS for instances that match your filters
resp = ec2.describe_instances(
    Filters=[
        {"Name": "instance-state-name",
            "Values": ["running"]},     # only running
        # optional: by tag
        {"Name": "tag:Name", "Values": ["PokemonGame4"]},
    ]
)

# 3. Walk the nested response and collect IDs
instance_ids = [
    inst["InstanceId"]
    for reservation in resp["Reservations"]
    for inst in reservation["Instances"]
]

print(instance_ids)   # ['i-0ab12c34de56f7890', ...]

INSTANCE_ID = instance_ids[0] if instance_ids else None

assocs = ec2.describe_iam_instance_profile_associations(
    Filters=[{"Name": "instance-id", "Values": [INSTANCE_ID]}]
)["IamInstanceProfileAssociations"]

if not assocs:
    ec2.associate_iam_instance_profile(
        InstanceId=INSTANCE_ID,
        IamInstanceProfile={"Name": PROFILE_NAME},
    )
    print("Profile attached")
else:
    ec2.replace_iam_instance_profile_association(
        AssociationId=assocs[0]["AssociationId"],
        IamInstanceProfile={"Name": PROFILE_NAME},
    )
    print("Profile replaced")
