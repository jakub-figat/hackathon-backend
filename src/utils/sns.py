import asyncio
from functools import partial

import boto3
from botocore.exceptions import ClientError


async def send_otp(phone_number: str, otp: int) -> None:
    sns = boto3.client("sns")

    try:
        publish = partial(sns.publish, PhoneNumber=phone_number, Message=f"OTP: {otp}")
        await asyncio.get_event_loop().run_in_executor(None, publish)
    except ClientError:
        pass
