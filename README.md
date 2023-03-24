# Service Account bulk session deletion for Rubrik API

## Purpose of the script

When working with service account within Rubrik there are a max sexxion count of 10 allowed. If sessions are not closed when using service accounts then the following error will likely be encountered.

*{"errorType":"user_error","message":"Max of 10 API Tokens reached.","cause":null}*

This can be caused by scripts exiting prematurely before closing sessions and various other reasons.

Service Account sessions are automatically closed after 24 hours when their token TTL is reached.

The script is used to close all open sessions in bulk to allow for continued use of the service account.

As best practice sessions should be closed at the end of scripts. This script should only be required for new users who may exhaust session count when testing Service Account functionality or where scripts are not correctly closing sessions.

## Requirements for user input

1. A temporary API token:
`https://<RUBRIK_IP>/web/bin/index.html#/api_tokens`
This token is required each time the script is ran
The token needs to be create by a user with the role: *AdministratorRole*

2. IP adress of the Rubrik cluster where the service account resides