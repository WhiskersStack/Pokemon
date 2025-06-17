import os
import boto3

def create_key_pair(ec2):
    # Create key pair
    key_pair_name = "MyKeyPair"

    try:
        response = ec2.create_key_pair(KeyName=key_pair_name)
    except Exception as e:
        print("\n\n\n ********************************** \n\n\n")
        print(f"Error creating key pair: {e}")
        print("\n\n\n ********************************** \n\n\n")
        return

    # Save private key to a .pem file
    with open(f"{key_pair_name}.pem", "w") as file:
        file.write(response["KeyMaterial"])

    # Set permissions (optional, but needed for SSH)
    os.chmod(f"{key_pair_name}.pem", 0o400)

    print(f"Key pair '{key_pair_name}' created and saved as '{key_pair_name}.pem'")

if __name__ == "__main__":
    create_key_pair(boto3.client("ec2", region_name="us-west-2"))
