from base64 import b64decode
import boto3

kms_client = boto3.client('kms')


def decrypt(secret):
    kms_response = kms_client.decrypt(
        CiphertextBlob=bytes(b64decode(secret))
    )
    return kms_response["Plaintext"].decode('utf-8')
