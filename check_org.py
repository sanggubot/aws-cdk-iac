# This Code is for check current AWS Organization information.
import os
import boto3
from dotenv import load_dotenv


def get_organization_info() -> (tuple | None):
    load_dotenv()  # Load environment variables from .env file

    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    client = session.client("organizations")

    try:
        response = client.describe_organization()

        organization_id = response["Organization"]["Id"]
        organization_ard = response["Organization"]["Arn"]
        organization_master_account_arn = response["Organization"]["MasterAccountArn"]
        organization_master_account_id = response["Organization"]["MasterAccountId"]
        organization_master_account_email = response["Organization"][
            "MasterAccountEmail"
        ]

        return (
            organization_id,
            organization_ard,
            organization_master_account_arn,
            organization_master_account_id,
            organization_master_account_email,
        )

    except client.exceptions.AWSOrganizationsNotInUseException:
        return None


if __name__ == "__main__":
    organization_info = get_organization_info()
    if organization_info:
        organization_id, accounts, root_id = organization_info
        print(f"Organization ID: {organization_id}")
        print(f"Accounts: {accounts}")
        print(f"Root ID: {root_id}")
    else:
        print("AWS Organizations is not enabled for this account.")
