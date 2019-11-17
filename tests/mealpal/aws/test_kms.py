from base64 import b64decode
from mealpal.aws.kms import decrypt


def test_decrypt(kms_stub):
    kms_stub.add_response(
        method='decrypt',
        service_response={
            'KeyId': 'keyId',
            'Plaintext': b'password',
            'ResponseMetadata': {}
        },
        expected_params={
            'CiphertextBlob': bytes(b64decode('ABCD'))
        },
    )

    actual_result = decrypt('ABCD')
    assert actual_result == 'password'
