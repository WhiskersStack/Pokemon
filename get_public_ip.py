import boto3
import time
import os


def get_public_ip(ec2, instance_id):
    # Wait a bit for the instance to be assigned a public IP
    print("\nWaiting for instance to be assigned a public IP...\n")
    time.sleep(10)

    # Describe instance to get full info
    desc = ec2.describe_instances(InstanceIds=[instance_id])
    public_ip = desc["Reservations"][0]["Instances"][0]["PublicIpAddress"]

    print("Public IP:", public_ip)

    # Save the public IP address to a file
    with open("public_ip.txt", "w") as file:
        file.write(public_ip)
    print(f"Public IP address saved to public_ip.txt")

    print("\nTo SSH into the instance, use the following command :\n")
    print(f"ssh -i MyKeyPair.pem ubuntu@{public_ip}\n")


if __name__ == "__main__":
    get_public_ip(boto3.client("ec2", region_name="us-west-2"), "i-0a1b2c3d4e5f6g7h8")