'''
Packages needed in default aws slack command blueprint
'''
import boto3, json, logging, os
'''
Packages non-native to lambda
Required to by installed, zipped with app, uploaded to lambda
'''
import req

'''
Environment variable decryption
'''
from base64 import b64decode
from urlparse import parse_qs
ENCRYPTED_EXPECTED_TOKEN = os.environ['kmsEncryptedToken']
kms = boto3.client('kms')
expected_token = kms.decrypt(CiphertextBlob=b64decode(ENCRYPTED_EXPECTED_TOKEN))['Plaintext']

'''
Logger setup
'''
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    params = parse_qs(event['body'])
    token = params['token'][0]
    if token != expected_token:
        logger.error("Request token (%s) does not match expected", token)
        return respond(Exception('Invalid request token'))

    user = params['user_name'][0]
    command = params['command'][0]
    channel = params['channel_name'][0]
    command_text = params['text'][0]

    return respond(None, "%s invoked %s in %s with the following text: %s" % (user, command, channel, command_text))
