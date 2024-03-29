# KeyVault Client Side Encryption Migration to Encryption Scope Server Side Encryption

This script functions as a sample of migrating data that was previously uploaded using client-side encryption with a KeyVault key to now use server-side encryption with an encryption scope using either a Microsoft managed key or a Customer managed key. The sample includes a script to generate sample data, `create_sample_data.py`, as well as a script that will migrate all data within a given container, `migration.py`.

## Getting Started
### Prerequisites
Requires installation of [Python 3](https://www.python.org/downloads/) and [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) (if you wish to programmatically generate an encryption scope). Requires an [Azure subscription](https://azure.microsoft.com/en-us/free/) and an [Azure storage account](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal).

This sample requires the following packages to be installed:
azure-storage-blob
azure-identity
azure-keyvault-keys
azure-keyvault-secrets

## Setup
#### Settings
The migration script and the sample data script require various settings about your Storage Account, Key Vault, etc. Please fill in the required values in `settings.py`.

### Creating sample data
The migration script expects some data to be set up ahead of time. Please see `create_sample_data.py` to see an example or to create sample data for testing. It is not required to run this file in order to run `migration.py`.

## Migration Script
Once setup is complete, the migration script, `migration.py` can be run to migrate all data within the provided container. The container name is provided in `settings.py`. Depending on the size of the container, this could take some time.