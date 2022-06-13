# Client Side Encryption to Server Side Encryption Migration

This directory contains samples for migrating from client-side encryption V1 to the various methods of server-side encryption.

**_NOTE_:** These samples are intended to be sample scripts to help in the process of migrating your data and should be reviewed and/or modified before being used to migrate any Production data.

Currently there are four samples present, each with their own directory:

- **ClientSideKeyVaultKeyToCustomerProvidedKey** - Migrate from client-side encryption V1 using a KeyVault to server-side encryption with a Customer-Provided Key.
- **ClientSideKeyVaultKeyToServerEncryptionScope** - Migrate from client-side encryption V1 using a KeyVault to server-side encryption with an Encryption Scope. The Encryption scope can be using a Microsoft managed key or a Customer managed key from KeyVault.
- **ClientSideLocalKeyToCustomerProvidedKey** - Migrate from client-side encryption V1 using a local key to server-side encryption with a Customer-Provided Key.
- **ClientSideLocalKeyToServerEncryptionScope** - Migrate from client-side encryption V1 using a local key to server-side encryption with an Encryption Scope. The Encryption scope can be using a Microsoft managed key or a Customer managed key from KeyVault.

## General Info
These samples begin with an optional data creation process to create an example container and populdate it with blobs encrypted with client-side encryption V1. The samples then migrate all blobs within the container to a specific type of server-side encryption and uploads the server-side encrypted blob in the same container (either alongside or overwritting the existing blobs). The sample data does not need to be used and the migration script can be used to migrate an existing cotnainer.

Each sample will contain the following files:
- `README.md` - Instructions more specific to the particular sample
- `settings.py` - Contains settings needed to run the sample. See below.
- `create_sample_data.py` - Script to generate sample data.
- `migration.py` - Script to migrate the data in a specific container.

## General Setup Requirements
All samples requires the following:
- Python >= 3.6
- The `azure-storage-blob` package to be installed
- An Azure Storage Account

Some sample may have additional requirements. See individual `README` for details.

Each sample contains a `settings.py` file that contains settings that must be specified in order to run the sample. These include settings about your Storage Account, KeyVault (if applicable), client-side encryption details, server-side encryption details, and some additional settings. These settings files must be populated before attempting to generate date or run the migration script.
