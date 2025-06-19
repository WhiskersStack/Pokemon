# Pokémon AWS Automation

This repository contains a small set of **Python 3** helper scripts that automate spinning up an EC2 instance, creating a DynamoDB table, and wiring everything together so you can experiment with Pokémon data on AWS.

---

## Features

- Create or ensure a DynamoDB table called **Pokemon** and seed it with a demo item  
  (`dynamoDB.py`).
- Generate an RSA key pair and download the PEM file locally  
  (`create_key_pair.py`).
- Launch an Ubuntu EC2 instance that clones the Pokémon demo repo on first boot  
  (`launch_ec2.py`).
- Open port 22 (SSH) on the instance’s security group  
  (`update_security_group.py`).
- Fetch and print the instance’s public IP address  
  (`get_public_ip.py`).
- (Optional) Attach or replace an IAM instance profile after launch  
  (`iam.py`).
- One‑shot orchestrator that glues everything together in sequence  
  (`ec2_init.py`).

---

## Prerequisites

```bash
# AWS CLI configured with credentials and default region
aws configure

# Python 3.11+ with virtualenv (recommended)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

You need AWS permissions for **ec2**, **dynamodb**, and **iam** actions described above.  
Default region inside the scripts is **us‑west‑2**—change it to suit your needs.

---

## Quick Start

```bash
# Bootstrap everything (key pair ▸ EC2 ▸ security group ▸ IP lookup)
python ec2_init.py
```

The script prints your *Instance ID* and *Public IP* when finished.

```bash
ssh -i MyKeyPair.pem ubuntu@<PublicIP>
```

---

## Script Reference

| Script                     | Purpose                                                                                                 |
|----------------------------|---------------------------------------------------------------------------------------------------------|
| `dynamoDB.py`              | Create a **Pokemon** DynamoDB table (partition key `id`, sort key `name`) and insert a demo item.       |
| `create_key_pair.py`       | Generate an EC2 key pair named **MyKeyPair** and save *MyKeyPair.pem* locally.                          |
| `launch_ec2.py`            | Launch an Ubuntu EC2 instance, tag it, and run a *user‑data* script that clones the Pokémon repo.       |
| `update_security_group.py` | Add an inbound SSH rule (TCP 22, 0.0.0.0/0) to the instance’s security group.                           |
| `get_public_ip.py`         | Look up and print the instance’s public IP address.                                                     |
| `iam.py`                   | Attach or swap an IAM instance profile on a running instance.                                          |
| `ec2_init.py`              | High‑level orchestrator that calls the above helpers in order.                                          |

---

## Project Structure

```
Pokemon-main/
 ├── .gitignore
 ├── .ssh/config
 ├── create_key_pair.py
 ├── dynamoDB.py
 ├── ec2_init.py
 ├── get_public_ip.py
 ├── iam.py
 ├── launch_ec2.py
 ├── requirements.txt
 ├── setup.py
 └── update_security_group.py
```

---

## Clean‑Up

```bash
# Terminate the instance
aws ec2 terminate-instances --instance-ids <InstanceID>

# Delete the key pair
aws ec2 delete-key-pair --key-name MyKeyPair
rm MyKeyPair.pem

# Remove the DynamoDB table
aws dynamodb delete-table --table-name Pokemon
```

---

## Roadmap

- Parameterise region, key name, and instance type via CLI args.
- Add CloudWatch logging and alarms.
- Switch infrastructure definition to AWS CDK or Terraform.
- Add unit tests with **moto** for local mocking.

---

## License

MIT
