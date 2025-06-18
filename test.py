#!/usr/bin/env python3
"""
create_dynamodb_table.py

End-to-end example:
  • Creates a DynamoDB table
  • Waits for it to become ACTIVE
  • Puts a demo item
  • Reads the same item back

Prerequisites:
  • `pip install boto3`
  • AWS credentials with dynamodb:CreateTable, dynamodb:PutItem, etc.
    (via `aws configure` or an IAM role/instance profile)

Run:
  python create_dynamodb_table.py --region us-west-2 --table Movies
"""
import argparse
import sys
import time
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


def create_table(dynamodb, table_name: str):
    """
    Create a simple on-demand table (year HASH, title RANGE).
    Returns the Table resource.
    """
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "year", "KeyType": "HASH"},   # partition key
                {"AttributeName": "title", "KeyType": "RANGE"}  # sort key
            ],
            AttributeDefinitions=[
                {"AttributeName": "year", "AttributeType": "N"},
                {"AttributeName": "title", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST",   # on-demand pricing
        )
        print(f"🛠️  Creating table '{table_name}' …")
        table.wait_until_exists()           # blocks until status == ACTIVE
        print(f"✅ Table '{table_name}' is ACTIVE")
        return table

    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print(f"⚠️  Table '{table_name}' already exists – using it")
            return dynamodb.Table(table_name)
        raise                              # bubble up anything else


def put_demo_item(table):
    """Insert a demo movie and fetch it back."""
    item = {
        "year": 1994,
        "title": "The Shawshank Redemption",
        "genre": "Drama"
    }
    print("➕ Putting demo item …")
    table.put_item(Item=item)

    print("🔎 Getting the same item back …")
    resp = table.get_item(Key={"year": item["year"], "title": item["title"]})
    print("🎉 Fetched item:", resp.get("Item"))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a DynamoDB table and test it")
    parser.add_argument("--region", required=True,
                        help="AWS Region, e.g. us-west-2")
    parser.add_argument("--table", default="Movies",
                        help="Table name (default: Movies)")
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        dynamodb = boto3.resource("dynamodb", region_name=args.region)
    except NoCredentialsError:
        print("❌ No AWS credentials found. Run `aws configure` or set env vars.", file=sys.stderr)
        sys.exit(1)

    table = create_table(dynamodb, args.table)
    put_demo_item(table)


if __name__ == "__main__":
    main()
