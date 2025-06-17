import boto3


def update_security_group(ec2, security_group_id):
    # Add SSH (port 22) rule to allow all IPs (0.0.0.0/0)

    try:
        ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": 22,
                    "ToPort": 22,
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                }
            ],
        )

        print("SSH access (port 22) added to security group")
    except Exception as e:
        print("\n\n\n ************************* \n\n\n")
        print(f"Error adding SSH access to security group: {e}")
        print("\n\n\n ************************* \n\n\n")


if __name__ == "__main__":
    update_security_group(boto3.client("ec2", region_name="us-west-2"))
