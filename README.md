# discord_bot
A bot for Brandon and I to harass our league with

## Run pipenv shell

### pre-reqs
- python 3.7
- pipenv

[RTFM](https://pipenv-fork.readthedocs.io/en/latest/basics.html#example-pipenv-workflow)

Hint:

```
$ pipenv install --dev
$ pipenv shell
```

## Upload lambda to AWS

### pre-reqs
- you'll need some AWS credentials with lambda upload permission (talk to Brandon)
- [install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

Configure the CLI (set the default region to `us-east-1`)

```
$ aws configure
```

Run this from the root of the project directory

```
$ ./uploadToLambda.sh
```
