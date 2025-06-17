# EC2 Automation Toolkit

Automates provisioning of an Amazon EC2 instance, SSH key pair, security‑group ingress, and retrieval of the public IP address so you can log in and immediately run your Pokémon game.

## Features

- **Key pair provisioning** – creates (or reuses) `MyKeyPair.pem` on AWS and saves the private key locally.
- **Instance launch** – starts a tagged **t2.micro** Amazon Linux 2 instance (AMI ID configurable) and injects user‑data that clones your GitHub repo and adds an auto‑run line to `~/.bashrc`.
- **Security‑group update** – opens port 22 (SSH) so you can connect at once.
- **Public‑IP discovery** – waits for the elastic IP and writes it to `public_ip.txt`, printing an `ssh` command for convenience.
- **One‑command bootstrap** – `setup.py` builds a virtual environment, installs requirements, and runs the entire workflow.

## Project Layout

```
.
├── create_key_pair.py          # Create or reuse SSH key pair
├── launch_ec2.py               # Launch EC2 and return instance + SG IDs
├── update_security_group.py    # Open port 22 for SSH
├── get_public_ip.py            # Poll for the public IP and save to file
├── ec2_init.py                 # Orchestrates the above utilities
├── setup.py                    # Creates venv, installs deps, runs ec2_init.py
├── requirements.txt            # Python dependencies (boto3 + friends)
└── public_ip.txt               # Filled automatically after launch
```

## Prerequisites

- Python 3.8 or newer
- An AWS account with programmatic access
- Local credentials configured via `aws configure` *or* the environment variables
  `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_DEFAULT_REGION`
- A valid Amazon Linux 2 AMI ID in your chosen region (default scripts use **us‑west‑2**)

## Quick Start

```bash
# 1 – Clone the repository
git clone https://github.com/<your‑account>/<repo‑name>.git
cd <repo‑name>

# 2 – Run the bootstrap script (creates venv → installs deps → provisions EC2)
python setup.py
```

The workflow:

1. **Virtual environment** created in `./venv`.
2. **Dependencies** installed from `requirements.txt`.
3. **ec2_init.py** executes and sequentially:
   - creates/validates the key pair `MyKeyPair`;
   - launches an instance called *PokemonGame1*;
   - opens SSH to `0.0.0.0/0` (adjust later for security);
   - fetches the public IPv4 address and saves it.

When complete you’ll see something like:

```bash
ssh -i MyKeyPair.pem ubuntu@<PUBLIC_IP>
```

Use that command to connect.

## Customisation Guide

| Task                                   | Location to edit                      |
|----------------------------------------|---------------------------------------|
| Instance type                          | `InstanceType` in **launch_ec2.py**   |
| AMI ID                                 | `ImageId` in **launch_ec2.py**        |
| Key‑pair name                          | `key_pair_name` in **create_key_pair.py** |
| Repo cloned on the instance            | `user_data_script` in **launch_ec2.py** |
| Ingress CIDR (restrict SSH source)     | `IpRanges` in **update_security_group.py** |

## Cleanup Commands

```bash
# Terminate the EC2 instance
aws ec2 terminate-instances --instance-ids <INSTANCE_ID>

# Delete the security group (only if no resources are attached)
aws ec2 delete-security-group --group-id <SECURITY_GROUP_ID>

# Remove key pair locally and in AWS
aws ec2 delete-key-pair --key-name MyKeyPair
rm -f MyKeyPair.pem
```

## Troubleshooting

- **`IndexError: list index out of range`** – the AMI ID is invalid in the chosen region; supply a correct ID.
- **`Permission denied (publickey)`** – ensure `chmod 400 MyKeyPair.pem` and that you are using the right username (`ubuntu`).

## License

MIT — see `LICENSE` for details.

## Acknowledgements

Built with [boto3](https://github.com/boto/boto3).
