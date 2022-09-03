#!/bin/bash
# remove old lambda.zip
rm lambda.zip

SITE_PACKAGES=$(pipenv --venv)/lib/python3.7/site-packages
echo "Library Location: $SITE_PACKAGES"
DIR=$(pwd)

# Make sure pipenv is good to go
pipenv install

cd $SITE_PACKAGES
zip -r9q $DIR/lambda.zip *

cd $DIR/lambda
zip -g $DIR/lambda.zip lambda_function.py

echo "uploading to lambda"
cd $DIR
PAGER=cat aws lambda update-function-code --function-name discord --zip-file fileb://lambda.zip
