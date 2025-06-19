import boto3
import os
import json
from botocore.exceptions import ClientError

def launch_ec2_instance(ec2):
    # Launch EC2 instance

    user_data_script = """#!/bin/bash
    cd /home/ubuntu
    git clone https://github.com/WhiskersStack/PokemonGameV2.git
    chown -R ubuntu:ubuntu /home/ubuntu/PokemonGameV2
    echo 'if [ -n "$SSH_CONNECTION" ]; then cd ~/PokemonGameV2 && python3 main.py; fi' >> /home/ubuntu/.bashrc
    """
    # echo 'if [ -n "$SSH_CONNECTION" ]; then python3 ~/PokemonGameV2/main.py; fi' >> ~/.bashrc

    response = ec2.run_instances(
        # Amazon Linux 2 AMI (check region-specific AMIs)
        ImageId="ami-075686beab831bb7f",
        InstanceType="t2.micro",
        KeyName="MyKeyPair",
        MinCount=1,
        MaxCount=1,
        UserData=user_data_script,
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {
                        "Key": "Name",
                        "Value": "PokemonGame",
                    }
                ]
            }
        ]
    )

    # Print instance security group ID
    instance_id = response["Instances"][0]["InstanceId"]
    print(f"Instance ID: {instance_id}")
    print(f"Security Group ID: {response['Instances'][0]['SecurityGroups'][0]['GroupId']}")
    security_group_id = response["Instances"][0]["SecurityGroups"][0]["GroupId"]

    ids = [instance_id, security_group_id]

    return ids

if __name__ == "__main__":
    launch_ec2_instance(boto3.client("ec2", region_name="us-west-2"))
