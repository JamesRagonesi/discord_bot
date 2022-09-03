from lambda_function import *
import json

new_video = open('test_data/new_video_payload.json')
sub_verify = open('test_data/subscription_verification_payload.json')

# new video payload
lambda_handler(json.load(new_video), {})

# subscription verification payload
lambda_handler(json.load(sub_verify), {})

# unsupported event
lambda_handler({}, {})

# unsupport body
lambda_handler({ "body": "body body" }, {})
