# Authorization Code Flow + PKCE Python Sample and Test

**Version:** 1.0.10

[![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/osisoft.sample-ocs-authentication_authorization-python?repoName=osisoft%2Fsample-ocs-authentication_authorization-python&branchName=main)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=2611&repoName=osisoft%2Fsample-ocs-authentication_authorization-python&branchName=main)

This sample uses the OAuth2/OIDC Authorization Code Flow + PKCE to obtain an access token. See the main OCS Authentication samples page [README](https://github.com/osisoft/OSI-Samples-OCS/blob/main/docs/AUTHENTICATION_README.md) for more information about this flow.

Developed against Python 3.8.2

## Python SDS Library

The [Python SDS library](https://github.com/osisoft/sample-ocs-sample_libraries-python), `ocs_sample_library_preview`, implements this flow inside its `OCSClient` type using the same Python code used in this sample. This sample is preserved separately to demonstrate that code in an isolated environment, and also to allow injection of a Selenium script for automated testing.

To use the Authorization Code Flow + PKCE flow with the library, pass a client ID for an OCS Authorization Code client, without a client secret, to the constructor. The libary will use this OIDC flow if no secret is passed to the constructor.

## Requirements

- Python 3
- Web Browser with Javascript enabled
  - Google Chrome Web Driver is required for the automated test
- Register an Authorization Code Client in OSIsoft Cloud Services and ensure that the registered client in OCS contains `http://localhost:5004/callback.html` in the list of RedirectUris
- Configure the sample using the file [config.placeholder.ini](config.placeholder.ini). Before editing, rename this file to `config.ini`. This repository's `.gitignore` rules should prevent the file from ever being checked in to any fork or branch, to ensure credentials are not compromised.
- Replace the placeholders in `config.ini` with your Tenant ID and Client ID

## Running the Sample

1. Open a command prompt in this folder
1. Install requirements, using `pip install -r requirements.txt`
1. Set up the `Configuration` section of the `config.ini` file, as described above
1. Run the sample using `python ./program.py`
1. Follow prompts in the browser to log in, if you are already logged in this step will be skipped
1. When prompted by the browser, return to the command prompt and a token will be logged

## Running the Automated Test

1. Open a command prompt in this folder
1. Install pytest, using `pip install pytest`
1. Install selenium, using `pip install selenium`
1. Set up the `Configuration` section of the `config.ini` file, as described above, if you have not already
1. Set up the `Test` section of the `config.ini` file with a username and password for the test to use to log in
1. Run the test, using `python -m pytest ./test.py`
1. Chrome should run in the background and log in, and the test will assert that a token is obtained

---

For the main OCS Authentication samples page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS/blob/main/docs/AUTHENTICATION_README.md)  
For the main OCS samples page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)  
For the main OSIsoft samples page [ReadMe](https://github.com/osisoft/OSI-Samples)
