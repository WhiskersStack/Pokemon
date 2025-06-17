import boto3
from launch_ec2 import launch_ec2_instance
from update_security_group import update_security_group
from create_key_pair import create_key_pair
from get_public_ip import get_public_ip


ec2 = boto3.client("ec2", region_name="us-west-2")


def main():
    # Create a key pair
    create_key_pair(ec2)

    # Launch an EC2 instance & get instance ID
    ids = launch_ec2_instance(ec2)
    print("EC2 instance launched successfully.")

    # Update security group to allow SSH access
    update_security_group(ec2, ids[1])

    # Get the public IP address of the instance
    get_public_ip(ec2, ids[0])

if __name__ == "__main__":
    main()


# aws ec2 delete-key-pair --key-name MyKeyPair
# ssh -i MyKeyPair.pem ubuntu@<PublicIP>
