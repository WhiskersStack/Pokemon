#!/usr/bin/env python3
import boto3
import botocore

INSTANCE_ID = "i-07e6e6af87c226c4f"
PROFILE_NAME = "LabInstanceProfile"
REGION = "us-west-2"

ec2 = boto3.client("ec2", region_name=REGION)

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
